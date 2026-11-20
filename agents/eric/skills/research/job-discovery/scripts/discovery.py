#!/usr/bin/env python3
"""Public vacancy collection; manual screening remains authoritative."""
import hashlib
import argparse
from collections import Counter
import sys
import fcntl
import os
import tempfile
from contextlib import contextmanager
import gzip
import time
import uuid
from datetime import datetime, timezone
import json
import re
from html import unescape
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen
from pathlib import Path
import xml.etree.ElementTree as ET


MAX_BYTES = 64 * 1024 * 1024


def fetch_url(url, *, timeout=20, max_bytes=MAX_BYTES, data=None, headers=None):
    parts = urlsplit(url)
    if parts.scheme not in ('http', 'https') or not parts.hostname or parts.username or parts.password:
        raise ValueError('Only public HTTP(S) URLs without credentials are supported')
    request_headers = {'User-Agent': 'JobDiscovery/1.0', 'Accept-Encoding': 'identity'}
    if headers:
        request_headers.update(headers)
    request = Request(url, data=data, headers=request_headers)
    with urlopen(request, timeout=timeout) as response:
        raw = response.read(max_bytes + 1)
    if len(raw) > max_bytes:
        raise ValueError('Response size limit exceeded')
    return raw


def post_url(url, payload, headers=None):
    request_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    if headers:
        request_headers.update(headers)
    return fetch_url(url, data=json.dumps(payload).encode('utf-8'), headers=request_headers)


def location_scope(location, country=None, remote=False):
    text = location.casefold()
    country = (country or '').casefold()
    us = country in ('us', 'usa', 'united states') or bool(re.search(r'\b(us|usa|united states|virginia|va|illinois)\b', text))
    region = country in ('', 'eu', 'europe', 'european union', 'global', 'worldwide', 'emea')
    if us:
        return 'out_of_scope'
    if country in ('at', 'aut', 'austria'):
        return 'in_scope'
    if re.search(r'\baustria\b', text):
        return 'in_scope' if region else 'location_review'
    if region and re.search(r'\b(wien|vienna)\b', text):
        return 'in_scope'
    if region and (not text or re.search(r'\b(europe|european|global|worldwide|remote|emea|anywhere)\b', text)):
        return 'location_review'
    return 'out_of_scope'


def plain(value):
    return ' '.join(unescape(re.sub(r'<[^>]+>', ' ', unescape(value or ''))).split())


def smartrecruiters(source, fetch, tracked, status):
    """Keep validated positive pages even when later pagination/details fail."""
    rows, seen_ids = [], set()
    url = source['url']
    offset, total = 0, None
    try:
        for unused in range(1000):
            payload = json.loads(fetch(url))
            jobs = payload['content']
            if not isinstance(jobs, list) or not jobs:
                raise ValueError('Empty or invalid SmartRecruiters page')
            if payload['offset'] != offset or type(payload['totalFound']) is not int:
                raise ValueError('Invalid pagination metadata')
            if total is not None and total != payload['totalFound']:
                raise ValueError('Pagination total changed during fetch')
            total = payload['totalFound']
            status['count'] += len(jobs)
            status['pages'] += 1
            for job in jobs:
                try:
                    identifier = job['id']
                    if not isinstance(identifier, str) or not re.fullmatch(r'[0-9]+', identifier):
                        raise ValueError('Invalid numeric SmartRecruiters id')
                    if identifier in seen_ids:
                        raise ValueError('Duplicate posting across pages')
                    seen_ids.add(identifier)
                    loc = job['location']
                    text = loc.get('fullLocation') or loc.get('city', '')
                    scope = location_scope(text, loc.get('country'), loc.get('remote', False))
                    if scope != 'out_of_scope' or source['id'] + ':' + identifier in tracked:
                        if not job.get('jobAd', {}).get('sections'):
                            detail_url = source['url'].split('?')[0].rstrip('/') + '/' + identifier
                            detail = json.loads(fetch(detail_url))
                            if detail.get('id') != identifier:
                                raise ValueError('Exact detail id mismatch')
                            job = detail
                            loc = job['location']
                            text = loc.get('fullLocation') or loc.get('city', '')
                        description = plain(' '.join(s.get('text', '') for s in job['jobAd']['sections'].values()))
                        if not description:
                            raise ValueError('Missing exact description')
                    else:
                        description = ''
                    rows.append(dict(id=identifier, title=job['name'], location=text,
                                     isRemote=loc.get('remote', False), isListed=True,
                                     jobUrl=job.get('postingUrl') or job.get('ref', ''),
                                     descriptionPlain=description, requisitionId=job.get('refNumber'),
                                     address={'postalAddress': {'addressCountry': loc.get('country')}},
                                     publishedAt=job.get('releasedDate')))
                except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
                    status['errors'].append(str(exc))
            offset += len(jobs)
            if offset == total:
                status['complete'] = not status['errors']
                break
            if offset > total:
                raise ValueError('Pagination exceeds total')
            parts = urlsplit(source['url'])
            query = dict(parse_qsl(parts.query))
            query.update(limit='100', offset=str(offset))
            url = urlunsplit(parts._replace(query=urlencode(query)))
        else:
            raise ValueError('Pagination limit reached')
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        status['errors'].append(str(exc))
    return {'jobs': rows}


def greenhouse(payload, status):
    rows = []
    for job in payload['jobs']:
        try:
            identifier = job['id']
            if type(identifier) is int and identifier > 0:
                identifier = str(identifier)
            if not isinstance(identifier, str) or not re.fullmatch(r'[0-9]+', identifier):
                raise ValueError('Invalid numeric Greenhouse id')
            description = plain(job['content'])
            if not description:
                raise ValueError('Greenhouse content missing; use jobs?content=true')
            rows.append(dict(id=identifier, title=job['title'], location=job['location']['name'],
                             isRemote=False, jobUrl=job['absolute_url'], descriptionPlain=description,
                             requisitionId=job.get('requisition_id'), publishedAt=job.get('first_published')))
        except (ValueError, TypeError, KeyError, AttributeError) as exc:
            status['complete'] = False
            status['errors'].append(str(exc))
    return {'jobs': rows}


def personio(raw, source, status):
    if b'<!DOCTYPE' in raw.upper() or b'<!ENTITY' in raw.upper():
        raise ValueError('XML declarations/entities not permitted')
    root = ET.fromstring(raw)
    if root.tag != 'workzag-jobs' or not root.findall('position'):
        raise ValueError('Empty or invalid Personio feed')
    rows = []
    status.update(complete=True, count=len(root.findall('position')))
    for job in root.findall('position'):
        try:
            identifier = job.findtext('id') or ''
            if not re.fullmatch(r'[0-9]+', identifier):
                raise ValueError('Invalid numeric Personio id')
            url = job.findtext('url') or source['role_url_template'].format(id=identifier)
            description = plain(' '.join(' '.join(node.itertext()) for node in job.findall('jobDescriptions/jobDescription')))
            if not description:
                raise ValueError('Personio description missing')
            rows.append(dict(id=identifier, title=job.findtext('name'), location=job.findtext('office') or '',
                             isRemote=False, jobUrl=url, descriptionPlain=description,
                             publishedAt=job.findtext('createdAt')))
        except (ValueError, TypeError, KeyError, AttributeError) as exc:
            status['complete'] = False
            status['errors'].append(str(exc))
    return {'jobs': rows}


def recruitee(payload, status):
    offers = payload.get('offers') if isinstance(payload, dict) else None
    if not isinstance(offers, list) or not offers:
        raise ValueError('Empty or invalid Recruitee offers')
    rows = []
    status.update(complete=True, count=len(offers))
    for offer in offers:
        try:
            identifier = offer['id']
            if type(identifier) is int and identifier > 0:
                identifier = str(identifier)
            if not isinstance(identifier, str) or not re.fullmatch(r'[0-9]+', identifier):
                raise ValueError('Invalid numeric Recruitee id')
            if offer.get('state_code') not in ('published', '9'):
                raise ValueError('Recruitee offer is not an observed open state')
            description = plain(offer.get('description'))
            if not description:
                raise ValueError('Recruitee description missing')
            title, location, url = offer.get('title'), offer.get('location'), offer.get('careers_url')
            if not isinstance(title, str) or not title.strip() or not isinstance(location, str):
                raise ValueError('Invalid Recruitee title or location')
            if not isinstance(url, str) or urlsplit(url).scheme not in ('http', 'https') or not urlsplit(url).hostname:
                raise ValueError('Invalid Recruitee careers URL')
            country = offer.get('country')
            if country is not None and not isinstance(country, str):
                raise ValueError('Invalid Recruitee country')
            remote = offer.get('remote', False)
            if type(remote) is not bool:
                raise ValueError('Invalid Recruitee remote flag')
            rows.append(dict(id=identifier, title=title, location=location, isRemote=remote,
                             jobUrl=url, descriptionPlain=description,
                             address={'postalAddress': {'addressCountry': country}},
                             publishedAt=offer.get('published_at')))
        except (ValueError, TypeError, KeyError, AttributeError) as exc:
            status['complete'] = False
            status['errors'].append(str(exc))
    return {'jobs': rows}


def successfactors(source, fetch, tracked, status):
    """Collect a complete public SuccessFactors search, with exact details only when needed."""
    rows, seen_ids, expected_total = [], set(), None
    url = source['url']
    try:
        for unused in range(1000):
            raw = fetch(url).decode('utf-8', 'replace')
            marker = re.search(r'Results\s+(\d+)\s*(?:[–-]|&ndash;|&#8211;|to)\s*(\d+)\s+of\s+(\d+)', raw, re.I)
            table = re.search(r'<table\b[^>]*id=["\']searchresults["\'][^>]*>([\s\S]*?)</table>', raw, re.I)
            if not marker or not table:
                raise ValueError('Missing SuccessFactors result count or table')
            start, end, total = map(int, marker.groups())
            if start < 1 or end < start or total < end:
                raise ValueError('Invalid SuccessFactors result range')
            if expected_total is not None and expected_total != total:
                raise ValueError('SuccessFactors total changed during fetch')
            expected_total = total
            page_rows = re.findall(r'<tr\b[^>]*class=["\'][^"\']*\bdata-row\b[^"\']*["\'][^>]*>([\s\S]*?)</tr>', table.group(1), re.I)
            if len(page_rows) != end - start + 1:
                raise ValueError('SuccessFactors result-row count mismatch')
            for fragment in page_rows:
                link = re.search(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*class=["\'][^"\']*\bjobTitle-link\b[^"\']*["\'][^>]*>([\s\S]*?)</a>', fragment, re.I)
                if not link:
                    raise ValueError('Missing SuccessFactors job link')
                href, title = unescape(link.group(1)), plain(link.group(2))
                absolute_url = urljoin(url, href)
                identifier = re.search(r'/([0-9]+)/?$', urlsplit(absolute_url).path)
                if not identifier or identifier.group(1) in seen_ids:
                    raise ValueError('Invalid or duplicate SuccessFactors id')
                identifier = identifier.group(1)
                seen_ids.add(identifier)
                location_cell = re.search(r'<td\b[^>]*class=["\'][^"\']*\bcolLocation\b[^"\']*["\'][^>]*>([\s\S]*?)</td>', fragment, re.I)
                location = plain(location_cell.group(1)) if location_cell else ''
                if not location:
                    path_location = re.search(r'/job/([^/]+)', urlsplit(absolute_url).path, re.I)
                    location = unescape(path_location.group(1)).split('-')[0] if path_location else ''
                country = 'AT' if re.search(r'\b(AT|Austria)\b', location, re.I) else None
                scope = location_scope(location, country)
                detail_needed = scope != 'out_of_scope' or source['id'] + ':' + identifier in tracked
                rows.append(dict(id=identifier, title=title, location=location, isRemote=False,
                                 jobUrl=absolute_url, descriptionPlain='',
                                 address={'postalAddress': {'addressCountry': country}}, publishedAt=None,
                                 _detail_needed=detail_needed))
            status['pages'] += 1
            if end == total:
                if len(rows) != total:
                    raise ValueError('SuccessFactors total/result mismatch')
                status['count'] = total
                break
            parts = urlsplit(source['url'])
            query = dict(parse_qsl(parts.query, keep_blank_values=True))
            query['startrow'] = str(end)
            url = urlunsplit(parts._replace(query=urlencode(query)))
        else:
            raise ValueError('SuccessFactors pagination limit reached')
        for job in rows:
            if not job.pop('_detail_needed'):
                continue
            try:
                for attempt in range(2):
                    try:
                        detail = fetch(job['jobUrl']).decode('utf-8', 'replace')
                        break
                    except OSError:
                        if attempt:
                            raise
                description_match = re.search(r'<span\b[^>]*class=["\'][^"\']*\bjobdescription\b[^"\']*["\'][^>]*>([\s\S]*?)</span>', detail, re.I)
                job['descriptionPlain'] = plain(description_match.group(1)) if description_match else ''
                if not job['descriptionPlain']:
                    raise ValueError('SuccessFactors detail description missing')
                locality = re.search(r'<meta\b[^>]*itemprop=["\']addressLocality["\'][^>]*content=["\']([^"\']+)', detail, re.I)
                address_country = re.search(r'<meta\b[^>]*itemprop=["\']addressCountry["\'][^>]*content=["\']([^"\']+)', detail, re.I)
                date_posted = re.search(r'<meta\b[^>]*itemprop=["\']datePosted["\'][^>]*content=["\']([^"\']+)', detail, re.I)
                if locality:
                    job['location'] = unescape(locality.group(1))
                if address_country:
                    job['address']['postalAddress']['addressCountry'] = unescape(address_country.group(1))
                if date_posted:
                    job['publishedAt'] = unescape(date_posted.group(1))
            except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
                status['errors'].append(str(exc))
        status['complete'] = not status['errors']
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        status['errors'].append(str(exc))
    return {'jobs': rows}


def successfactors_json(source, post, fetch, tracked, status):
    """Collect a public SuccessFactors Recruiting JSON search and exact details."""
    rows, seen_ids, expected_total = [], set(), None
    locale = source.get('locale', 'en_US')
    try:
        for page_number in range(1000):
            request_payload = {'keywords': '', 'locale': locale, 'location': '',
                               'pageNumber': page_number, 'sortBy': 'recent'}
            payload = json.loads(post(source['url'], request_payload))
            total = payload.get('totalJobs')
            jobs = payload.get('jobSearchResult')
            if type(total) is not int or total < 1 or not isinstance(jobs, list) or not jobs:
                raise ValueError('Empty or invalid SuccessFactors Recruiting JSON page')
            if expected_total is not None and expected_total != total:
                raise ValueError('SuccessFactors Recruiting JSON total changed during fetch')
            expected_total = total
            for item in jobs:
                record = item['response']
                identifier = str(record['id'])
                if not identifier or identifier in seen_ids:
                    raise ValueError('Invalid or duplicate SuccessFactors Recruiting JSON id')
                seen_ids.add(identifier)
                title = plain(record['unifiedStandardTitle'])
                location = plain(' '.join(record.get('jobLocationShort', [])))
                country = 'AT' if re.search(r'\b(AUT|Austria)\b', location, re.I) else None
                parts = urlsplit(source['url'])
                slug = unescape(record['unifiedUrlTitle'])
                job_url = urlunsplit((parts.scheme, parts.netloc,
                                      '/job/' + slug + '/' + identifier + '-' + locale, '', ''))
                scope = location_scope(location, country)
                rows.append(dict(id=identifier, title=title, location=location, isRemote=False,
                                 jobUrl=job_url, descriptionPlain='',
                                 address={'postalAddress': {'addressCountry': country}}, publishedAt=None,
                                 _detail_needed=scope != 'out_of_scope' or source['id'] + ':' + identifier in tracked))
            status['pages'] += 1
            if len(rows) == total:
                status['count'] = total
                break
            if len(rows) > total:
                raise ValueError('SuccessFactors Recruiting JSON total/result mismatch')
        else:
            raise ValueError('SuccessFactors Recruiting JSON pagination limit reached')
        for job in rows:
            if not job.pop('_detail_needed'):
                continue
            try:
                for attempt in range(2):
                    try:
                        detail = fetch(job['jobUrl']).decode('utf-8', 'replace')
                        break
                    except OSError:
                        if attempt:
                            raise
                description_match = re.search(r'<div\b[^>]*class=["\'][^"\']*\bjobColumnOne\b[^"\']*["\'][^>]*>([\s\S]*?)<div\b[^>]*class=["\'][^"\']*\bjobColumnTwo\b', detail, re.I)
                job['descriptionPlain'] = plain(description_match.group(1)) if description_match else ''
                if not job['descriptionPlain']:
                    raise ValueError('SuccessFactors Recruiting JSON detail description missing')
            except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
                status['errors'].append(str(exc))
        status['complete'] = not status['errors']
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        status['errors'].append(str(exc))
    return {'jobs': rows}


def workday(source, fetch, post, tracked, status):
    """Collect one public Workday Candidate Experience board with a fresh page token."""
    rows, seen_ids, expected_total = [], set(), None
    try:
        board = fetch(source['url']).decode('utf-8', 'replace')
        token_match = re.search(r'\btoken\s*:\s*["\']([^"\']+)["\']', board)
        if not token_match:
            raise ValueError('Workday public page token missing')
        headers = {'Authorization': 'Bearer ' + token_match.group(1),
                   'Accept-Language': source.get('locale', 'en-US')}
        jobs_url = source['jobs_url']
        detail_base = jobs_url.rsplit('/jobs', 1)[0]
        board_parts = urlsplit(source['url'])
        board_path = board_parts.path
        if board_path.startswith('/' + source.get('locale', '') + '/'):
            board_path = board_path[len(source.get('locale', '')) + 1:]
        public_base = urlunsplit((board_parts.scheme, board_parts.netloc, board_path.rstrip('/'), '', ''))
        limit = source.get('page_size', 20)
        if type(limit) is not int or limit < 1 or limit > 100:
            raise ValueError('Invalid Workday page size')
        facets = {'locationCountry': [source['location_country']]}
        offset = 0
        for unused in range(1000):
            request_payload = {'appliedFacets': facets, 'limit': limit, 'offset': offset, 'searchText': ''}
            payload = json.loads(post(jobs_url, request_payload, headers))
            reported_total, jobs = payload.get('total'), payload.get('jobPostings')
            if type(reported_total) is not int or reported_total < 0 or not isinstance(jobs, list):
                raise ValueError('Invalid Workday listing page')
            if expected_total is None:
                if reported_total == 0 and jobs:
                    raise ValueError('Workday first listing page has zero total with results')
                expected_total = reported_total
            elif reported_total not in (0, expected_total):
                raise ValueError('Workday total changed during fetch')
            total = expected_total
            if total and not jobs:
                raise ValueError('Empty Workday listing page before total reached')
            remaining = total - len(rows)
            if len(jobs) > min(limit, remaining):
                raise ValueError('Workday listing page exceeds remaining total')
            for item in jobs:
                path = item['externalPath']
                title = plain(item['title'])
                identifiers = item.get('bulletFields')
                if (not isinstance(path, str) or not path.startswith('/job/') or '?' in path
                        or not title or not isinstance(identifiers, list) or len(identifiers) != 1
                        or not isinstance(identifiers[0], str) or not re.fullmatch(r'Req[0-9]+', identifiers[0])):
                    raise ValueError('Invalid Workday listing identity')
                identifier = identifiers[0]
                if identifier in seen_ids:
                    raise ValueError('Duplicate Workday requisition across pages')
                seen_ids.add(identifier)
                location = plain(item.get('locationsText', ''))
                country = 'AT' if re.search(r'\b(Austria|Österreich|Wien|Vienna)\b', location, re.I) else None
                scope = location_scope(location, country)
                rows.append(dict(id=identifier, title=title, location=location, isRemote=False,
                                 jobUrl=public_base + path, descriptionPlain='', publishedAt=None,
                                 _detail_url=detail_base + path, _detail_needed=(scope != 'out_of_scope'
                                 or source['id'] + ':' + identifier in tracked)))
            status['pages'] += 1
            if len(rows) == total:
                status['count'] = total
                break
            if len(rows) > total:
                raise ValueError('Workday total/result mismatch')
            offset += len(jobs)
        else:
            raise ValueError('Workday pagination limit reached')
        for job in rows:
            if not job.pop('_detail_needed'):
                job.pop('_detail_url')
                continue
            try:
                detail = json.loads(fetch(job.pop('_detail_url'), headers=headers))['jobPostingInfo']
                if detail.get('jobReqId') != job['id'] or plain(detail.get('title')) != job['title']:
                    raise ValueError('Workday detail identity mismatch')
                job_url = detail.get('externalUrl')
                if not isinstance(job_url, str) or urlsplit(job_url).scheme not in ('http', 'https') or not urlsplit(job_url).hostname:
                    raise ValueError('Workday canonical URL missing')
                description = plain(detail.get('jobDescription'))
                if not description:
                    raise ValueError('Workday detail description missing')
                country = detail.get('country')
                if isinstance(country, dict):
                    country = country.get('descriptor')
                if isinstance(country, str) and re.fullmatch(r'Austria|Österreich', country, re.I):
                    country = 'AT'
                job.update(jobUrl=job_url, descriptionPlain=description,
                           location=plain(detail.get('location') or job['location']),
                           address={'postalAddress': {'addressCountry': country}},
                           publishedAt=detail.get('posted'))
            except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
                status['errors'].append(str(exc))
        status['complete'] = not status['errors']
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        status['errors'].append(str(exc))
    return {'jobs': rows}


SEMANTIC = ('title', 'url', 'location', 'country', 'remote', 'description', 'family_key', 'locations')


def normalize_job(source, job, now):
    identifier = job['id']
    if not isinstance(identifier, str) or not re.fullmatch(r'\S+', identifier):
        raise ValueError('Invalid literal posting id')
    if not isinstance(job.get('title'), str) or not job['title'].strip():
        raise ValueError('Missing posting title')
    url = job['jobUrl']
    if not isinstance(url, str) or urlsplit(url).scheme not in ('http', 'https') or not urlsplit(url).hostname:
        raise ValueError('Missing/invalid original posting URL')
    remote, listed = job.get('isRemote'), job.get('isListed', True)
    remote = False if remote is None else remote
    if type(remote) is not bool or type(listed) is not bool:
        raise ValueError('Invalid remote/listed flags')
    description = job.get('descriptionPlain') or job.get('descriptionHtml') or ''
    if not isinstance(description, str):
        raise ValueError('Invalid description type')
    description = plain(description)
    secondary = job.get('secondaryLocations') or []
    if not isinstance(secondary, list):
        raise ValueError('Invalid secondary locations')
    locations = []
    for item in [job] + secondary:
        text = item.get('location', '')
        country = ((item.get('address') or {}).get('postalAddress') or {}).get('addressCountry')
        if not isinstance(text, str) or (country is not None and not isinstance(country, str)):
            raise ValueError('Invalid location/country type')
        if country is None and re.search(r'\baustria\b', text, flags=re.I):
            country = 'AT'
        locations.append({'location': text, 'country': country})
    scopes = {location_scope(loc['location'], loc['country'], remote) for loc in locations}
    scope = ('in_scope' if 'in_scope' in scopes else 'location_review' if 'location_review' in scopes else 'out_of_scope')
    if scope != 'out_of_scope' and not description:
        raise ValueError('Missing description for candidate/tracked observation')
    key = source['id'] + ':' + identifier
    ref = job.get('requisitionId') or identifier
    if type(ref) not in (str, int):
        raise ValueError('Invalid explicit requisition identity')
    row = dict(key=key, source_id=source['id'], posting_id=identifier,
               family_key=source['id'] + ':' + str(ref), employer=source['employer'], title=job['title'], url=url,
               location='; '.join(loc['location'] for loc in locations), locations=locations,
               country=locations[0]['country'] if len(locations) == 1 else None,
               remote=remote, description=description, location_scope=scope,
               availability='listed' if listed else 'not_listed', decision='unreviewed', reason='',
               application_record=None, evidence=[], first_seen=now, last_seen=now, last_checked=now,
               published_at=job.get('publishedAt'))
    row['fingerprint'] = hashlib.sha256(json.dumps({k: row[k] for k in SEMANTIC}, sort_keys=True).encode()).hexdigest()
    return row


def validate_document(payload, field):
    if not isinstance(payload, dict) or payload.get('schema_version') != 1 or not isinstance(payload.get(field), list):
        raise ValueError('Expected schema_version=1 and a ' + field + ' list')
    seen = set()
    for row in payload[field]:
        if not isinstance(row, dict):
            raise ValueError('Expected object in ' + field)
        identity = row.get('id' if field == 'sources' else 'key')
        if not isinstance(identity, str) or not identity or identity in seen:
            raise ValueError('Missing or duplicate identity in ' + field)
        seen.add(identity)
        if field == 'sources':
            if (not re.fullmatch(r'[A-Za-z0-9_-]+', identity)
                    or row.get('mode') not in ('automatic', 'manual')
                    or type(row.get('enabled')) is not bool
                    or row.get('priority') not in ('core', 'adjacent')
                    or not all(isinstance(row.get(k), str) for k in ('employer', 'adapter', 'url', 'notes'))):
                raise ValueError('Invalid source configuration: ' + identity)
        else:
            required = ('key', 'source_id', 'posting_id', 'family_key', 'employer', 'title', 'url',
                        'location', 'remote', 'description', 'fingerprint', 'availability', 'decision',
                        'reason', 'application_record', 'evidence', 'first_seen', 'last_seen', 'last_checked')
            if any(k not in row for k in required):
                raise ValueError('Missing required opportunity fields: ' + identity)
            if (not isinstance(row['posting_id'], str) or not row['posting_id']
                    or row['posting_id'] != row['posting_id'].strip()
                    or not isinstance(row['source_id'], str)
                    or identity != row['source_id'] + ':' + row['posting_id']
                    or row['decision'] not in DECISIONS
                    or row['availability'] not in ('listed', 'not_listed', 'closed', 'unknown')
                    or type(row['remote']) is not bool
                    or not isinstance(row['evidence'], list)):
                raise ValueError('Invalid opportunity contract: ' + identity)
    return payload[field]


def scoped(workspace, path):
    path = Path(path)
    if not path.resolve().is_relative_to(workspace):
        raise ValueError('Path escapes explicit workspace: ' + str(path))
    return path


def atomic_json(workspace, path, payload):
    path = scoped(workspace, path)
    name = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
                                         prefix='.' + path.name, suffix='.tmp', delete=False) as handle:
            name = handle.name
            json.dump(payload, handle, indent=2, ensure_ascii=False, allow_nan=False)
            handle.write('\n')
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(name, scoped(workspace, path))
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if name and Path(name).exists():
            Path(name).unlink()


@contextmanager
def workspace_lock(workspace):
    with scoped(workspace, workspace / '.discovery.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def refresh(workspace, *, apply=False, source_ids=None, fetch=None, post=None, now=None):
    workspace = Path(workspace).resolve(strict=True)
    fetch = fetch or fetch_url
    post = post or post_url
    with workspace_lock(workspace):
        return _refresh(workspace, apply=apply, source_ids=source_ids, fetch=fetch, post=post, now=now)


def _refresh(workspace, *, apply=False, source_ids=None, fetch=None, post=None, now=None):
    workspace = Path(workspace).resolve()
    registry_path = scoped(workspace, workspace / 'opportunities.json')
    registry_before = registry_path.read_bytes()
    now = now or datetime.now(timezone.utc).isoformat()
    day = datetime.fromisoformat(now.replace('Z', '+00:00')).date().isoformat()
    run_dir = scoped(workspace, workspace / 'runs' / day / uuid.uuid4().hex)
    run_dir.mkdir(parents=True)
    sources = validate_document(json.loads((workspace / 'sources.json').read_bytes()), 'sources')
    registry = json.loads(registry_before)
    validate_document(registry, 'opportunities')
    if source_ids and set(source_ids) - {s['id'] for s in sources}:
        raise ValueError('Unknown selected source id')
    events, statuses = [], []
    for source in sources:
        started = time.monotonic()
        status = {'id': source['id'], 'complete': False, 'count': 0, 'errors': [], 'status': 'failure',
                  'elapsed_seconds': 0, 'evidence': [], 'admitted': 0, 'suppressed': 0, 'pages': 0}
        def observed_fetch(url, headers=None):
            try:
                raw = fetch(url, headers=headers) if headers else fetch(url)
                evidence_raw = raw
                if source['adapter'] == 'workday' and url == source['url']:
                    evidence_raw = re.sub(rb'(\btoken\s*:\s*["\'])[^"\']+', rb'\1[REDACTED]', raw)
                artifact = run_dir / (str(len(statuses)) + '-' + str(len(status['evidence'])) + '.raw.gz')
                artifact.write_bytes(gzip.compress(evidence_raw, mtime=0))
                status['evidence'].append({'url': url, 'path': str(artifact),
                                           'sha256': hashlib.sha256(evidence_raw).hexdigest(), 'bytes': len(evidence_raw),
                                           'redacted': evidence_raw != raw} )
                return raw
            finally:
                status['elapsed_seconds'] = round(time.monotonic() - started, 6)
        def observed_post(url, request_payload, headers=None):
            try:
                raw = post(url, request_payload, headers=headers) if headers else post(url, request_payload)
                artifact = run_dir / (str(len(statuses)) + '-' + str(len(status['evidence'])) + '.raw.gz')
                artifact.write_bytes(gzip.compress(raw, mtime=0))
                status['evidence'].append({'url': url, 'method': 'POST', 'request_payload': request_payload,
                                           'path': str(artifact), 'sha256': hashlib.sha256(raw).hexdigest(),
                                           'bytes': len(raw)})
                return raw
            finally:
                status['elapsed_seconds'] = round(time.monotonic() - started, 6)
        statuses.append(status)
        skip = ('unselected' if source_ids and source['id'] not in source_ids else
                'disabled' if not source.get('enabled', True) else
                'manual' if source.get('mode') == 'manual' else None)
        if skip:
            status['status'] = skip
            continue
        try:
            if source['adapter'] == 'smartrecruiters':
                payload = smartrecruiters(source, observed_fetch, {r['key'] for r in registry['opportunities']}, status)
            elif source['adapter'] == 'personio':
                payload = personio(observed_fetch(source['url']), source, status)
            elif source['adapter'] == 'recruitee':
                payload = recruitee(json.loads(observed_fetch(source['url'])), status)
            elif source['adapter'] == 'successfactors':
                payload = successfactors(source, observed_fetch, {r['key'] for r in registry['opportunities']}, status)
            elif source['adapter'] == 'successfactors_json':
                payload = successfactors_json(source, observed_post, observed_fetch,
                                               {r['key'] for r in registry['opportunities']}, status)
            elif source['adapter'] == 'workday':
                payload = workday(source, observed_fetch, observed_post,
                                  {r['key'] for r in registry['opportunities']}, status)
            elif source['adapter'] in ('ashby', 'greenhouse'):
                payload = json.loads(observed_fetch(source['url']))
                if not isinstance(payload, dict) or not isinstance(payload.get('jobs'), list) or not payload['jobs']:
                    raise ValueError('Empty or invalid jobs; absence inference withheld')
                status.update(complete=True, count=len(payload['jobs']))
                if source['adapter'] == 'greenhouse':
                    payload = greenhouse(payload, status)
            else:
                raise ValueError('Unsupported automatic adapter: ' + str(source['adapter']))
        except (OSError, ValueError, TypeError, KeyError, AttributeError, ET.ParseError) as exc:
            status['errors'].append(str(exc))
            continue
        seen = set()
        for job in payload['jobs']:
            try:
                row = normalize_job(source, job, now)
                key = row['key']
                if key in seen:
                    raise ValueError('Duplicate posting identity')
                seen.add(key)
            except (ValueError, TypeError, KeyError, AttributeError) as exc:
                status['complete'] = False
                status['errors'].append(str(exc))
                continue
            old = next((r for r in registry['opportunities'] if r['key'] == key), None)
            if old is None:
                if row['location_scope'] == 'out_of_scope' or row['availability'] != 'listed':
                    status['suppressed'] += 1
                    continue
                status['admitted'] += 1
                row['evidence'] = [e['path'] for e in status['evidence']]
                registry['opportunities'].append(row)
                events.append({'key': key, 'kind': 'new'})
            else:
                baseline = old.get('fingerprint') is None
                material = bool(old.get('fingerprint')) and old['fingerprint'] != row['fingerprint']
                reopened = old.get('availability') in ('not_listed', 'closed') and row['availability'] == 'listed'
                if reopened:
                    events.append({'key': key, 'kind': 'reopened'})
                elif material:
                    events.append({'key': key, 'kind': 'changed'})
                if baseline or material or reopened:
                    old['evidence'] = list(dict.fromkeys(old['evidence'] + [e['path'] for e in status['evidence']]))
                if row['published_at'] is not None:
                    old['published_at'] = row['published_at']
                for k in (*SEMANTIC, 'location_scope', 'fingerprint', 'availability', 'last_seen', 'last_checked'):
                    old[k] = row[k]
        status['status'] = 'success' if status['complete'] else 'partial'
        for old in registry['opportunities']:
            if status['complete'] and old['source_id'] == source['id'] and old['key'] not in seen:
                old['availability'] = 'not_listed'
                old['last_checked'] = now
    if apply:
        if scoped(workspace, registry_path).read_bytes() != registry_before:
            raise RuntimeError('Registry changed during collection; refusing overwrite')
        atomic_json(workspace, registry_path, registry)
    protected = {r['key'] for r in registry['opportunities'] if r['decision'] in ('applied_reported', 'deferred')}
    result = {'sources': statuses, 'events': events, 'review_queue': [e['key'] for e in events if e['key'] not in protected],
              'backlog': [r['key'] for r in registry['opportunities'] if r['decision'] == 'unreviewed'],
              'applied': apply, 'checked_at': now, 'report_path': str(run_dir / 'report.json')}
    atomic_json(workspace, run_dir / 'report.json', result)
    return result


def report(workspace):
    workspace = Path(workspace).resolve(strict=True)
    rows = validate_document(json.loads(scoped(workspace, workspace / 'opportunities.json').read_bytes()), 'opportunities')
    return {'total': len(rows), 'decisions': dict(Counter(r['decision'] for r in rows)),
            'availability': dict(Counter(r['availability'] for r in rows)), 'events': [],
            'backlog': [r['key'] for r in rows if r['decision'] == 'unreviewed'],
            'unresolved': [{k: r.get(k) for k in ('key', 'employer', 'title', 'availability', 'location_scope')}
                           for r in rows if r['decision'] == 'unreviewed']}


DECISIONS = ('unreviewed', 'shortlisted', 'reviewed', 'excluded', 'deferred', 'applied_reported')


def review(workspace, *, key, decision, reason, evidence=None, application_record=None):
    if decision not in DECISIONS or not isinstance(reason, str) or not reason.strip():
        raise ValueError('A valid decision and nonempty reason are required')
    workspace = Path(workspace).resolve(strict=True)
    with workspace_lock(workspace):
        path = scoped(workspace, workspace / 'opportunities.json')
        before = path.read_bytes()
        registry = json.loads(before)
        validate_document(registry, 'opportunities')
        row = next((r for r in registry['opportunities'] if r['key'] == key), None)
        if row is None:
            raise ValueError('Unknown literal opportunity key')
        row.update(decision=decision, reason=reason)
        if evidence is not None and evidence not in row['evidence']:
            row['evidence'].append(evidence)
        if application_record is not None:
            row['application_record'] = application_record
        if path.read_bytes() != before:
            raise RuntimeError('Registry changed during review')
        atomic_json(workspace, path, registry)
        return row


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    refresh_parser = commands.add_parser('refresh', help='Collect/diff; registry writes require --apply')
    refresh_parser.add_argument('--workspace', required=True, type=Path)
    refresh_parser.add_argument('--source', action='append', dest='source_ids')
    refresh_parser.add_argument('--apply', action='store_true')
    report_parser = commands.add_parser('report', help='Current register and unresolved backlog; no new events')
    report_parser.add_argument('--workspace', required=True, type=Path)
    review_parser = commands.add_parser('review', help='Atomically update human decision and canonical references only')
    review_parser.add_argument('--workspace', required=True, type=Path)
    review_parser.add_argument('--key', required=True)
    review_parser.add_argument('--decision', required=True, choices=DECISIONS)
    review_parser.add_argument('--reason', required=True)
    review_parser.add_argument('--evidence')
    review_parser.add_argument('--application-record')
    args = vars(parser.parse_args(argv))
    command = args.pop('command')
    try:
        result = {'refresh': refresh, 'report': report, 'review': review}[command](**args)
    except (OSError, ValueError, RuntimeError, KeyError) as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return int(any(s['status'] in ('failure', 'partial') for s in result.get('sources', [])))


if __name__ == '__main__':
    raise SystemExit(main())

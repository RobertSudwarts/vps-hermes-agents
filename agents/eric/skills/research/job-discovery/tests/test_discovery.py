"""Offline tests. Synthetic vacancies are edge cases, not real leads."""
import importlib.util
import json
from pathlib import Path
import tempfile
import types
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'discovery.py'
if SCRIPT.exists():
    spec = importlib.util.spec_from_file_location('discovery', SCRIPT)
    discovery = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(discovery)
else:
    discovery = types.SimpleNamespace()


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / 'tests')
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name)
        self.source = dict(id='synthetic', employer='Synthetic employer', adapter='ashby',
                           url='https://example.test/feed', mode='automatic', enabled=True,
                           priority='core', notes='Synthetic edge-case fixture')
        self.save('sources.json', {'schema_version': 1, 'sources': [self.source]})
        self.save('opportunities.json', {'schema_version': 1, 'opportunities': []})
        self.job = dict(id='literal-001', title='Synthetic Engineer', location='Vienna, Austria',
                        isRemote=False, jobUrl='https://example.test/jobs/literal-001',
                        descriptionPlain='Synthetic job description', isListed=True)
        self.payload = {'jobs': [self.job]}

    def save(self, name, data):
        (self.workspace / name).write_text(json.dumps(data), encoding='utf-8')

    def load(self):
        return json.loads((self.workspace / 'opportunities.json').read_text())

    def refresh(self, **kwargs):
        return discovery.refresh(self.workspace, fetch=lambda url: json.dumps(self.payload).encode(),
                                 now='2026-11-13T12:00:00Z', **kwargs)

    def test_first_refresh_admits_in_scope_literal_identity(self):
        self.assertTrue(callable(getattr(discovery, 'refresh', None)), 'refresh API is missing')
        result = self.refresh(apply=True)
        row = self.load()['opportunities'][0]
        self.assertEqual(row['key'], 'synthetic:literal-001')
        self.assertEqual(row['posting_id'], 'literal-001')
        self.assertEqual(row['family_key'], row['key'])
        self.assertEqual(row['decision'], 'unreviewed')
        self.assertEqual(row['availability'], 'listed')
        self.assertEqual(row['location_scope'], 'in_scope')
        self.assertEqual([e['kind'] for e in result['events']], ['new'])
        for field in ('source_id', 'employer', 'title', 'url', 'location', 'remote', 'description',
                      'fingerprint', 'reason', 'application_record', 'evidence', 'first_seen',
                      'last_seen', 'last_checked'):
            self.assertIn(field, row)

    def test_repeat_has_no_events_but_keeps_unreviewed_backlog(self):
        self.refresh(apply=True)
        self.job['publishedAt'] = '2026-11-14T00:00:00Z'
        result = self.refresh(apply=True)
        self.assertEqual(result['events'], [])
        self.assertEqual(len(self.load()['opportunities']), 1)
        self.assertEqual(result['backlog'], ['synthetic:literal-001'])
        self.assertEqual(result['review_queue'], [])

    def test_baseline_then_material_changes_preserve_manual_fields(self):
        self.refresh(apply=True)
        registry = self.load()
        row = registry['opportunities'][0]
        row.update(fingerprint=None, decision='excluded', reason='Historical screening',
                   application_record='/canonical/existing.md', custom={'keep': True},
                   evidence=['/existing/evidence'], first_seen='2020-01-01T00:00:00Z')
        self.save('opportunities.json', registry)
        self.assertEqual(self.refresh(apply=True)['events'], [])
        self.job['descriptionPlain'] += ' materially changed'
        changed = self.refresh(apply=True)
        self.assertEqual([e['kind'] for e in changed['events']], ['changed'])
        self.assertEqual(changed['review_queue'], ['synthetic:literal-001'])
        row = self.load()['opportunities'][0]
        self.assertEqual(row['decision'], 'excluded')
        self.assertEqual(row['custom'], {'keep': True})
        self.assertIn('/existing/evidence', row['evidence'])
        self.assertEqual(row['application_record'], '/canonical/existing.md')
        self.assertEqual(row['first_seen'], '2020-01-01T00:00:00Z')
        for decision in ('applied_reported', 'deferred'):
            registry = self.load()
            registry['opportunities'][0]['decision'] = decision
            self.save('opportunities.json', registry)
            self.job['descriptionPlain'] += ' another change'
            self.assertEqual(self.refresh(apply=True)['review_queue'], [])
            self.assertEqual(self.load()['opportunities'][0]['decision'], decision)

    def test_location_triage_keeps_variants_without_claiming_remote_eligibility(self):
        self.job['requisitionId'] = 'REQ-shared'
        self.payload['jobs'] += [dict(self.job, id='foreign', location='New York, US', isRemote=True),
                                 dict(self.job, id='remote', location='Europe', isRemote=True),
                                 dict(self.job, id='us-vienna', location='Vienna, Virginia, US'),
                                 dict(self.job, id='local', location='Wien')]
        self.refresh(apply=True)
        rows = {r['posting_id']: r for r in self.load()['opportunities']}
        self.assertEqual(set(rows), {'literal-001', 'remote', 'local'})
        self.assertEqual(rows['remote']['location_scope'], 'location_review')
        self.assertEqual({r['family_key'] for r in rows.values()}, {'synthetic:REQ-shared'})
        self.job['location'] = 'Berlin, Germany'
        result = self.refresh(apply=True)
        row = next(r for r in self.load()['opportunities'] if r['posting_id'] == 'literal-001')
        self.assertEqual(row['location_scope'], 'out_of_scope')
        self.assertIn('changed', [e['kind'] for e in result['events']])

    def test_failure_never_infers_absence_but_complete_feed_can(self):
        self.refresh(apply=True)
        registry = self.load()
        registry['opportunities'][0]['decision'] = 'applied_reported'
        reference = dict(registry['opportunities'][0], key='hays:901137/1', source_id='hays', posting_id='901137/1')
        registry['opportunities'].append(reference)
        self.save('opportunities.json', registry)
        def broken(url):
            raise OSError('synthetic offline failure')
        try:
            result = discovery.refresh(self.workspace, apply=True, fetch=broken, now='2026-11-14T00:00:00Z')
        except OSError:
            self.fail('source failures must become incomplete statuses, not abort refresh')
        self.assertFalse(result['sources'][0]['complete'])
        self.assertEqual(self.load()['opportunities'][0]['availability'], 'listed')
        self.payload = {'jobs': []}
        self.assertFalse(self.refresh(apply=True)['sources'][0]['complete'])
        self.payload = {'jobs': [dict(self.job, id='other', location='Berlin, Germany')]}
        self.assertTrue(self.refresh(apply=True)['sources'][0]['complete'])
        self.assertEqual(self.load()['opportunities'][0]['availability'], 'not_listed')
        self.assertEqual(self.load()['opportunities'][1], reference)
        self.payload = {'jobs': [self.job]}
        result = self.refresh(apply=True)
        self.assertEqual([e['kind'] for e in result['events']], ['reopened'])
        self.assertEqual(result['review_queue'], [])
        self.assertEqual(self.load()['opportunities'][0]['decision'], 'applied_reported')

    def test_malformed_rows_allow_positive_observations_not_absence_inference(self):
        self.refresh(apply=True)
        for bad_id in ('', ' padded ', None, 1.2, True, {'id': 'x'}):
            self.payload = {'jobs': [dict(self.job, id='good-new'), dict(self.job, id=bad_id)]}
            try:
                result = self.refresh(apply=True)
            except (TypeError, KeyError, ValueError):
                self.fail('malformed adapter rows must be reported, not crash or normalized')
            self.assertFalse(result['sources'][0]['complete'])
            rows = self.load()['opportunities']
            self.assertEqual({r['posting_id'] for r in rows}, {'literal-001', 'good-new'})
            self.assertEqual(rows[0]['availability'], 'listed')
        self.payload = {'jobs': [dict(self.job, isListed=False)]}
        self.refresh(apply=True)
        self.assertEqual(self.load()['opportunities'][0]['availability'], 'not_listed')

    def test_saved_real_smartrecruiters_pages_scope_before_exact_details(self):
        evidence = Path('/vault/eric/Research/finance-tech/2026-11-13/evidence')
        self.source.update(id='scalable', adapter='smartrecruiters',
                           url='https://api.smartrecruiters.com/v1/companies/ScalableGmbH/postings?limit=100&offset=0')
        self.save('sources.json', {'schema_version': 1, 'sources': [self.source]})
        pages = {0: (evidence / 'scalable-feed.html').read_bytes(),
                 100: (evidence / 'scalable-feed-2.html').read_bytes()}
        from urllib.parse import urlsplit, parse_qs
        requested = []
        def fetch(url):
            requested.append(url)
            if '?' in url:
                return pages[int(parse_qs(urlsplit(url).query)['offset'][0])]
            if url.endswith('/744000157997674'):
                return (evidence / 'scalable-vienna-api.html').read_bytes()
            raise OSError('No preserved exact detail for this role; intentionally offline')
        result = discovery.refresh(self.workspace, apply=True, fetch=fetch, now='2026-11-13T12:00:00Z')
        self.assertEqual(result['sources'][0]['count'], 110)
        self.assertFalse(result['sources'][0]['complete'])  # four exact details not preserved
        rows = self.load()['opportunities']
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row['posting_id'], '744000157997674')
        self.assertEqual(row['family_key'], 'scalable:REF498E')
        self.assertEqual(row['location_scope'], 'in_scope')
        self.assertIn('Python', row['description'])
        self.assertTrue(row['url'].startswith('https://jobs.smartrecruiters.com/'))
        self.assertEqual(len([u for u in requested if '?' not in u]), 5)
        self.assertEqual(discovery.refresh(self.workspace, apply=True, fetch=fetch)['events'], [])

    def test_greenhouse_preserved_real_detail_wrapped_as_feed(self):
        detail = json.loads(Path('/vault/eric/Research/finance-tech/2026-11-13/evidence/bybit-institutional-api.html').read_bytes())
        self.source.update(id='bybit', adapter='greenhouse')
        self.save('sources.json', {'schema_version': 1, 'sources': [self.source]})
        self.payload = {'jobs': [detail]}  # actual preserved detail, synthetic feed envelope
        result = self.refresh(apply=True)
        self.assertTrue(result['sources'][0]['complete'])
        row = self.load()['opportunities'][0]
        self.assertEqual(row['posting_id'], '4966770101')
        self.assertEqual(row['family_key'], 'bybit:589')
        self.assertEqual(row['url'], detail['absolute_url'])
        self.assertNotIn('<div', row['description'])
        self.assertIn('Trading', row['description'])
        self.assertEqual(row['published_at'], detail['first_published'])
        detail['updated_at'] = '2030-01-01T00:00:00Z'
        self.assertEqual(self.refresh(apply=True)['events'], [])

    def test_saved_real_ashby_full_feed_has_normalized_text_and_stable_repeat(self):
        raw = Path('/vault/eric/Research/vienna-roles/2026-11-13/evidence/bjak-feed.raw').read_bytes()
        self.source.update(id='bjak', adapter='ashby')
        self.save('sources.json', {'schema_version': 1, 'sources': [self.source]})
        try:
            result = discovery.refresh(self.workspace, apply=True, fetch=lambda url: raw)
        except AttributeError as exc:
            self.fail('real Ashby null optional addresses must parse: ' + str(exc))
        self.assertTrue(result['sources'][0]['complete'])
        self.assertEqual(result['sources'][0]['count'], 3156)
        rows = self.load()['opportunities']
        self.assertTrue(rows)
        self.assertLess(len(rows), 3156)
        self.assertTrue(all('\n' not in r['description'] for r in rows))
        self.assertTrue(all(r['url'].startswith('https://jobs.ashbyhq.com/bjakcareer/') for r in rows))
        self.assertEqual(discovery.refresh(self.workspace, apply=True, fetch=lambda url: raw)['events'], [])

    def test_personio_xml_uses_office_and_explicit_role_url_template(self):
        self.source.update(adapter='personio', role_url_template='https://example.test/job/{id}?language=en')
        self.save('sources.json', {'schema_version': 1, 'sources': [self.source]})
        raw = b'''<workzag-jobs><position><id>2776596</id><name>Synthetic engineer</name>
        <office>Austria</office><createdAt>2026-10-01</createdAt><jobDescriptions><jobDescription>
        <name>About</name><value><![CDATA[<p>Synthetic description</p>]]></value>
        </jobDescription></jobDescriptions></position></workzag-jobs>'''
        result = discovery.refresh(self.workspace, apply=True, fetch=lambda url: raw)
        self.assertTrue(result['sources'][0]['complete'])
        row = self.load()['opportunities'][0]
        self.assertEqual(row['posting_id'], '2776596')
        self.assertEqual(row['url'], 'https://example.test/job/2776596?language=en')
        self.assertEqual(row['location_scope'], 'in_scope')
        self.assertEqual(row['description'], 'About Synthetic description')
        self.assertEqual(discovery.refresh(self.workspace, apply=True, fetch=lambda url: raw)['events'], [])

    def test_recruitee_public_offer_uses_canonical_url_and_full_description(self):
        self.source.update(adapter='recruitee')
        self.save('sources.json', {'schema_version': 1, 'sources': [self.source]})
        self.payload = {'offers': [{
            'id': 2816982,
            'title': 'Synthetic Recruitee Engineer',
            'state_code': 'published',
            'location': 'Wien, Wien, Austria',
            'country': 'Austria',
            'remote': False,
            'careers_url': 'https://synthetic.recruitee.com/o/synthetic-recruitee-engineer',
            'description': '<p>Build <strong>reliable</strong> financial systems.</p>',
            'published_at': '2026-11-05 12:52:23 UTC',
        }]}
        result = self.refresh(apply=True)
        self.assertTrue(result['sources'][0]['complete'])
        self.assertEqual(result['sources'][0]['count'], 1)
        row = self.load()['opportunities'][0]
        self.assertEqual(row['posting_id'], '2816982')
        self.assertEqual(row['url'], 'https://synthetic.recruitee.com/o/synthetic-recruitee-engineer')
        self.assertEqual(row['location_scope'], 'in_scope')
        self.assertEqual(row['description'], 'Build reliable financial systems.')
        self.assertEqual(row['published_at'], '2026-11-05 12:52:23 UTC')

    def test_recruitee_open_numeric_state_from_live_feed_is_admitted(self):
        self.source.update(adapter='recruitee')
        self.save('sources.json', {'schema_version': 1, 'sources': [self.source]})
        self.payload = {'offers': [{
            'id': 2816982,
            'title': 'Synthetic Live-State Engineer',
            'state_code': '9',
            'location': 'Wien, Wien, Austria',
            'country': 'Austria',
            'remote': True,
            'careers_url': 'https://synthetic.recruitee.com/o/synthetic-live-state-engineer',
            'description': '<p>Structured public offer.</p>',
            'published_at': '2026-11-06 07:04:28 UTC',
        }]}
        result = self.refresh(apply=True)
        self.assertTrue(result['sources'][0]['complete'])
        self.assertEqual(result['sources'][0]['count'], 1)
        self.assertEqual(self.load()['opportunities'][0]['posting_id'], '2816982')

    def test_successfactors_paginates_and_reads_in_scope_detail(self):
        self.source.update(adapter='successfactors', url='https://example.test/search/?q=')
        self.save('sources.json', {'schema_version': 1, 'sources': [self.source]})
        first = b'''<table id="searchresults" aria-label="Results 1 to 1 of 2"><tbody>
        <tr class="data-row"><td class="colTitle"><a href="/job/Vienna-Engineer/1001/" class="jobTitle-link">Vienna Engineer</a></td>
        <td class="colLocation"><span class="jobLocation">Vienna, AT</span></td></tr></tbody></table>'''
        second = b'''<table id="searchresults" aria-label="Results 2 - 2 of 2"><tbody>
        <tr class="data-row"><td class="colTitle"><a href="/job/Berlin-Engineer/1002/" class="jobTitle-link">Berlin Engineer</a></td>
        <td class="colLocation"><span class="jobLocation">Berlin, DE</span></td></tr></tbody></table>'''
        detail = b'''<meta itemprop="addressLocality" content="Vienna"><meta itemprop="addressCountry" content="AT">
        <span itemprop="description" class="jobdescription"><div><div></div><h2></h2><p>Build <strong>safe</strong> systems.</p></div></span>'''
        requested = []
        pages = {
            'https://example.test/search/?q=': first,
            'https://example.test/search/?q=&startrow=1': second,
            'https://example.test/job/Vienna-Engineer/1001/': detail,
        }
        def fetch(url):
            requested.append(url)
            if url.endswith('/1001/') and requested.count(url) == 1:
                raise TimeoutError('transient detail timeout')
            return pages[url]
        result = discovery.refresh(self.workspace, apply=True, fetch=fetch, now='2026-11-13T12:00:00Z')
        self.assertTrue(result['sources'][0]['complete'])
        self.assertEqual(result['sources'][0]['count'], 2)
        self.assertEqual(result['sources'][0]['pages'], 2)
        self.assertEqual(requested, list(pages) + ['https://example.test/job/Vienna-Engineer/1001/'])
        row = self.load()['opportunities'][0]
        self.assertEqual(row['posting_id'], '1001')
        self.assertEqual(row['location'], 'Vienna')
        self.assertEqual(row['country'], 'AT')
        self.assertEqual(row['description'], 'Build safe systems.')

    def test_successfactors_recruiting_json_reconciles_pages_and_reads_details(self):
        source = dict(self.source, adapter='successfactors_json',
                      url='https://example.test/services/recruiting/v1/jobs', locale='en_US')
        def result(identifier, title, location, slug):
            return {'response': {'id': identifier, 'unifiedStandardTitle': title,
                                 'jobLocationShort': [location], 'unifiedUrlTitle': slug}}
        pages = {
            0: {'totalJobs': 3, 'jobSearchResult': [
                result('1001', 'Vienna Engineer', 'Vienna, AUT, 1100<br/>', 'Vienna-Engineer'),
                result('1002', 'Berlin Engineer', 'Berlin, DE, 10115<br/>', 'Berlin-Engineer')]},
            1: {'totalJobs': 3, 'jobSearchResult': [
                result('1003', 'Vienna Analyst', 'Vienna, AUT, 1100<br/>', 'Vienna-Analyst')]},
        }
        requested_pages, requested_details = [], []
        def post(url, payload):
            self.assertEqual(url, source['url'])
            requested_pages.append(payload['pageNumber'])
            return json.dumps(pages[payload['pageNumber']]).encode()
        def fetch(url):
            requested_details.append(url)
            return b'''<div class="jobColumnOne"><div><p>Exact <strong>role</strong> description.</p></div></div>
                        <div class="jobColumnTwo">'''
        status = {'count': 0, 'pages': 0, 'errors': [], 'complete': False}
        payload = discovery.successfactors_json(source, post, fetch, set(), status)
        self.assertTrue(status['complete'])
        self.assertEqual((status['count'], status['pages'], status['errors']), (3, 2, []))
        self.assertEqual(requested_pages, [0, 1])
        self.assertEqual(len(requested_details), 2)
        self.assertEqual([j['id'] for j in payload['jobs']], ['1001', '1002', '1003'])
        self.assertEqual(payload['jobs'][0]['descriptionPlain'], 'Exact role description.')
        self.assertEqual(payload['jobs'][1]['descriptionPlain'], '')

    def test_successfactors_recruiting_json_refresh_records_post_evidence(self):
        self.source.update(adapter='successfactors_json', url='https://example.test/services/recruiting/v1/jobs', locale='en_US')
        self.save('sources.json', {'schema_version': 1, 'sources': [self.source]})
        page = {'totalJobs': 1, 'jobSearchResult': [{'response': {
            'id': '1001', 'unifiedStandardTitle': 'Vienna Engineer',
            'jobLocationShort': ['Vienna, AUT, 1100<br/>'], 'unifiedUrlTitle': 'Vienna-Engineer'}}]}
        def post(url, payload):
            self.assertEqual((url, payload['pageNumber']), (self.source['url'], 0))
            return json.dumps(page).encode()
        def fetch(url):
            self.assertEqual(url, 'https://example.test/job/Vienna-Engineer/1001-en_US')
            return b'''<div class="jobColumnOne"><p>Complete description.</p></div><div class="jobColumnTwo">'''
        result = discovery.refresh(self.workspace, apply=True, fetch=fetch, post=post,
                                   now='2026-11-13T12:00:00Z')
        status = result['sources'][0]
        self.assertTrue(status['complete'])
        self.assertEqual(status['evidence'][0]['method'], 'POST')
        self.assertEqual(status['evidence'][0]['request_payload']['pageNumber'], 0)
        self.assertEqual(self.load()['opportunities'][0]['description'], 'Complete description.')

    def test_workday_reconciles_pages_uses_fresh_page_token_and_reads_exact_detail(self):
        source = dict(self.source, adapter='workday',
                      url='https://example.test/de-DE/SyntheticCareers',
                      jobs_url='https://example.test/wday/cxs/synthetic/SyntheticCareers/jobs',
                      location_country='austria-facet', locale='de-DE')
        page = b'''<script>window.workday = { token: "fresh-public-token" };</script>'''
        pages = {
            0: {'total': 3, 'jobPostings': [
                {'title': 'Vienna Engineer', 'externalPath': '/job/Vienna/Vienna-Engineer_Req1001',
                 'locationsText': 'Vienna', 'postedOn': 'Posted Today', 'bulletFields': ['Req1001']},
                {'title': 'Berlin Engineer', 'externalPath': '/job/Berlin/Berlin-Engineer_Req1002',
                 'locationsText': 'Berlin', 'postedOn': 'Posted Today', 'bulletFields': ['Req1002']}]},
            2: {'total': 0, 'jobPostings': [
                {'title': 'Berlin Analyst', 'externalPath': '/job/Berlin/Berlin-Analyst_Req1003',
                 'locationsText': 'Berlin', 'postedOn': 'Posted Today', 'bulletFields': ['Req1003']}]},
        }
        details = {
            'https://example.test/wday/cxs/synthetic/SyntheticCareers/job/Vienna/Vienna-Engineer_Req1001': {
                'jobPostingInfo': {'id': 'opaque-1', 'jobReqId': 'Req1001', 'title': 'Vienna Engineer',
                                   'location': 'Vienna', 'country': {'descriptor': 'Austria', 'id': 'austria-facet'},
                                   'externalUrl': 'https://example.test/SyntheticCareers/job/Vienna/Vienna-Engineer_Req1001',
                                   'jobDescription': '<p>Exact <strong>role</strong> description.</p>',
                                   'posted': '2026-11-13'}}}
        requested_pages, requested_details = [], []
        def fetch(url, headers=None):
            if url == source['url']:
                self.assertIsNone(headers)
                return page
            requested_details.append((url, headers))
            return json.dumps(details[url]).encode()
        def post(url, payload, headers=None):
            self.assertEqual(url, source['jobs_url'])
            self.assertEqual(headers['Authorization'], 'Bearer fresh-public-token')
            self.assertEqual(payload['appliedFacets'], {'locationCountry': ['austria-facet']})
            requested_pages.append(payload['offset'])
            return json.dumps(pages[payload['offset']]).encode()
        status = {'count': 0, 'pages': 0, 'errors': [], 'complete': False}
        payload = discovery.workday(source, fetch, post, set(), status)
        self.assertTrue(status['complete'])
        self.assertEqual((status['count'], status['pages'], status['errors']), (3, 2, []))
        self.assertEqual(requested_pages, [0, 2])
        self.assertEqual(len(requested_details), 1)
        self.assertEqual(requested_details[0][1]['Authorization'], 'Bearer fresh-public-token')
        self.assertEqual([job['id'] for job in payload['jobs']], ['Req1001', 'Req1002', 'Req1003'])
        self.assertEqual(payload['jobs'][0]['jobUrl'], details[requested_details[0][0]]['jobPostingInfo']['externalUrl'])
        self.assertEqual(payload['jobs'][0]['descriptionPlain'], 'Exact role description.')
        self.assertEqual(payload['jobs'][0]['address']['postalAddress']['addressCountry'], 'AT')
        self.assertEqual(payload['jobs'][1]['descriptionPlain'], '')

    def test_manual_disabled_and_unselected_sources_are_explicitly_skipped(self):
        sources = [self.source, dict(self.source, id='manual', mode='manual'),
                   dict(self.source, id='disabled', enabled=False), dict(self.source, id='other')]
        self.save('sources.json', {'schema_version': 1, 'sources': sources})
        original = (self.workspace / 'sources.json').read_bytes()
        called = []
        def fetch(url):
            called.append(url)
            return json.dumps(self.payload).encode()
        result = discovery.refresh(self.workspace, apply=True, source_ids=['synthetic', 'manual', 'disabled'], fetch=fetch)
        self.assertEqual(len(called), 1)
        self.assertEqual({s['id']: s['status'] for s in result['sources']},
                         {'synthetic': 'success', 'manual': 'manual', 'disabled': 'disabled', 'other': 'unselected'})
        self.assertEqual((self.workspace / 'sources.json').read_bytes(), original)
        with self.assertRaises(ValueError):
            discovery.refresh(self.workspace, source_ids=['typo'], fetch=fetch)

    def test_dry_run_saves_actual_fetch_evidence_and_report_without_registry_write(self):
        import gzip
        original = (self.workspace / 'opportunities.json').read_bytes()
        result = self.refresh()
        self.assertEqual((self.workspace / 'opportunities.json').read_bytes(), original)
        self.assertIn('report_path', result, 'dry run must persist an auditable report')
        saved = json.loads(Path(result['report_path']).read_text())
        self.assertFalse(saved['applied'])
        status = saved['sources'][0]
        self.assertGreaterEqual(status['elapsed_seconds'], 0)
        self.assertEqual(status['admitted'], 1)
        self.assertEqual(len(status['evidence']), 1)
        artifact = Path(status['evidence'][0]['path'])
        self.assertTrue(artifact.is_relative_to(self.workspace))
        self.assertEqual(json.loads(gzip.decompress(artifact.read_bytes())), self.payload)
        self.assertEqual(status['evidence'][0]['url'], self.source['url'])
        self.assertEqual(saved['events'], result['events'])

    def test_writes_are_scoped_locked_and_reject_concurrent_registry_edits(self):
        import fcntl
        with (self.workspace / '.discovery.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaises((ValueError, RuntimeError, BlockingIOError)):
                self.refresh(apply=True)
        original = self.load()
        def concurrent(url):
            self.save('opportunities.json', dict(original, manual_note='Concurrent human edit'))
            return json.dumps(self.payload).encode()
        with self.assertRaises((ValueError, RuntimeError)):
            discovery.refresh(self.workspace, apply=True, fetch=concurrent)
        self.assertEqual(self.load()['manual_note'], 'Concurrent human edit')
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as outside:
            target = Path(outside) / 'protected.json'
            target.write_text(json.dumps(original))
            (self.workspace / 'opportunities.json').unlink()
            (self.workspace / 'opportunities.json').symlink_to(target)
            with self.assertRaises(ValueError):
                self.refresh(apply=True)
            self.assertEqual(json.loads(target.read_text()), original)

    def test_failed_atomic_replace_leaves_registry_intact(self):
        from unittest.mock import patch
        original = (self.workspace / 'opportunities.json').read_bytes()
        with patch('os.replace', side_effect=OSError('synthetic replace interruption')):
            with self.assertRaises(OSError):
                self.refresh(apply=True)
        self.assertEqual((self.workspace / 'opportunities.json').read_bytes(), original)
        self.assertEqual(list(self.workspace.glob('*.tmp')), [])

    def test_default_http_fetch_is_bounded_and_refresh_uses_it(self):
        import http.server
        import threading
        self.assertTrue(callable(getattr(discovery, 'fetch_url', None)), 'bounded HTTP transport is missing')
        payload = json.dumps(self.payload).encode()
        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(payload)
            def log_message(self, *args):
                pass
        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        self.source['url'] = 'http://127.0.0.1:%s/feed' % server.server_port
        self.save('sources.json', {'schema_version': 1, 'sources': [self.source]})
        self.assertEqual(discovery.fetch_url(self.source['url'], timeout=2, max_bytes=len(payload)), payload)
        with self.assertRaises(ValueError):
            discovery.fetch_url(self.source['url'], timeout=2, max_bytes=10)
        with self.assertRaises(ValueError):
            discovery.fetch_url('file:///etc/passwd')
        self.assertTrue(discovery.refresh(self.workspace, apply=True)['sources'][0]['complete'])

    def test_cli_help_and_report_expose_backlog_without_relabeling_it_new(self):
        import subprocess
        import sys
        help_result = subprocess.run([sys.executable, '-B', str(SCRIPT), '--help'], capture_output=True, text=True)
        self.assertEqual(help_result.returncode, 0)
        self.assertIn('refresh', help_result.stdout)
        self.assertIn('report', help_result.stdout)
        self.refresh(apply=True)
        self.assertTrue(callable(getattr(discovery, 'report', None)), 'report API is missing')
        summary = discovery.report(self.workspace)
        self.assertEqual(summary['total'], 1)
        self.assertEqual(summary['backlog'], ['synthetic:literal-001'])
        self.assertEqual(summary['events'], [])
        result = subprocess.run([sys.executable, '-B', str(SCRIPT), 'report', '--workspace', str(self.workspace)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), summary)

    def test_review_cli_updates_only_manual_fields_with_literal_reference_key(self):
        import subprocess
        import sys
        self.refresh(apply=True)
        registry = self.load()
        row = registry['opportunities'][0]
        row.update(key='hays:901137/1', posting_id='901137/1', source_id='hays', family_key='hays:901137/1', custom='keep')
        self.save('opportunities.json', registry)
        result = subprocess.run([sys.executable, '-B', str(SCRIPT), 'review', '--workspace', str(self.workspace),
                                 '--key', row['key'], '--decision', 'applied_reported', '--reason', 'User reported submission',
                                 '--evidence', '/canonical/proof.md', '--application-record', '/canonical/application.md'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        updated = self.load()['opportunities'][0]
        expected = dict(row, decision='applied_reported', reason='User reported submission',
                        evidence=row['evidence'] + ['/canonical/proof.md'], application_record='/canonical/application.md')
        self.assertEqual(updated, expected)
        self.assertEqual(discovery.report(self.workspace)['backlog'], [])
        with self.assertRaises(ValueError):
            discovery.review(self.workspace, key=row['key'], decision='invalid', reason='No')
        with self.assertRaises(ValueError):
            discovery.review(self.workspace, key='missing', decision='reviewed', reason='No')

    def test_broken_payloads_do_not_abort_other_sources_or_fake_completeness(self):
        good = dict(self.source, id='good', url='https://example.test/good')
        cases = [('ashby', b'[]'), ('ashby', b'{"jobs":null}'),
                 ('personio', b'<workzag-jobs><position>'), ('unknown', json.dumps(self.payload).encode()),
                 ('ashby', json.dumps({'jobs': [dict(self.job, address='broken')]}).encode()),
                 ('ashby', json.dumps({'jobs': [self.job, self.job]}).encode())]
        for adapter, raw in cases:
            with self.subTest(adapter=adapter, raw=raw[:60]):
                self.source['adapter'] = adapter
                self.save('sources.json', {'schema_version': 1, 'sources': [self.source, good]})
                self.save('opportunities.json', {'schema_version': 1, 'opportunities': []})
                def fetch(url):
                    return json.dumps(self.payload).encode() if url == good['url'] else raw
                try:
                    result = discovery.refresh(self.workspace, apply=True, fetch=fetch)
                except Exception as exc:
                    self.fail('broken public payload aborted other sources: ' + repr(exc))
                self.assertFalse(result['sources'][0]['complete'])
                self.assertTrue(result['sources'][1]['complete'])
                self.assertIn('good:literal-001', [r['key'] for r in self.load()['opportunities']])

    def test_scope_uses_secondary_advertised_locations_without_erasing_variants(self):
        self.job.update(location='Berlin, Germany', address={'postalAddress': {'addressCountry': 'DE'}},
                        secondaryLocations=[{'location': 'Vienna, Austria', 'address': {'postalAddress': {'addressCountry': 'AT'}}}])
        result = self.refresh(apply=True)
        self.assertEqual(len(result['events']), 1)
        row = self.load()['opportunities'][0]
        self.assertIn('Berlin', row['location'])
        self.assertIn('Vienna', row['location'])
        self.assertEqual(row['location_scope'], 'in_scope')
        self.assertEqual(len(row['locations']), 2)
        self.job['secondaryLocations'] = []
        self.assertEqual([e['kind'] for e in self.refresh(apply=True)['events']], ['changed'])
        self.assertEqual(self.load()['opportunities'][0]['location_scope'], 'out_of_scope')

    def test_invalid_registry_or_source_schema_refuses_writes_before_fetch(self):
        called = []
        def fetch(url):
            called.append(url)
            return json.dumps(self.payload).encode()
        empty = {'schema_version': 1, 'opportunities': []}
        cases = [(dict(schema_version=2, opportunities=[]), [self.source]),
                 (empty, [self.source, self.source])]
        self.refresh(apply=True)
        row = self.load()['opportunities'][0]
        for changes in ({'posting_id': 123}, {'key': 'wrong:identity'}, {'decision': 'invented'}):
            cases.append((dict(schema_version=1, opportunities=[dict(row, **changes)]), [self.source]))
        cases.append((dict(schema_version=1, opportunities=[row, row]), [self.source]))
        for registry, sources in cases:
            with self.subTest(registry=registry.get('schema_version'), sources=len(sources)):
                self.save('sources.json', {'schema_version': 1, 'sources': sources})
                self.save('opportunities.json', registry)
                before = (self.workspace / 'opportunities.json').read_bytes()
                with self.assertRaises(ValueError):
                    discovery.refresh(self.workspace, apply=True, fetch=fetch)
                self.assertEqual((self.workspace / 'opportunities.json').read_bytes(), before)
        self.assertEqual(called, [])

    def test_paginated_partial_feed_reports_pages_without_marking_absence(self):
        self.source.update(adapter='smartrecruiters', url='https://example.test/postings?limit=100&offset=0')
        self.save('sources.json', {'schema_version': 1, 'sources': [self.source]})
        def job(identifier, city):
            return dict(id=identifier, name='Synthetic engineer', refNumber='REF-shared',
                        location={'city': city, 'country': 'at', 'remote': False},
                        postingUrl='https://example.test/job/' + identifier,
                        jobAd={'sections': {'jobDescription': {'text': '<p>Synthetic duties</p>'}}})
        jobs = [job('101', 'Wien'), job('102', 'Vienna')]
        feed = {'offset': 0, 'limit': 100, 'totalFound': 2, 'content': jobs}
        result = discovery.refresh(self.workspace, apply=True, fetch=lambda url: json.dumps(feed).encode())
        self.assertTrue(result['sources'][0]['complete'])
        self.assertIn('pages', result['sources'][0], 'pagination needs observable page accounting')
        self.assertEqual(result['sources'][0]['pages'], 1)
        registry = self.load()
        registry['opportunities'][1]['decision'] = 'applied_reported'
        self.save('opportunities.json', registry)
        feed['content'] = jobs[:1]
        def partial(url):
            if 'offset=0' in url:
                return json.dumps(feed).encode()
            raise OSError('Synthetic second-page failure')
        result = discovery.refresh(self.workspace, apply=True, fetch=partial)
        self.assertFalse(result['sources'][0]['complete'])
        self.assertEqual(result['sources'][0]['pages'], 1)
        self.assertEqual(self.load()['opportunities'][1]['availability'], 'listed')
        feed['totalFound'] = 1
        discovery.refresh(self.workspace, apply=True, fetch=lambda url: json.dumps(feed).encode())
        self.assertEqual(self.load()['opportunities'][1]['availability'], 'not_listed')
        feed.update(content=jobs, totalFound=2)
        result = discovery.refresh(self.workspace, apply=True, fetch=lambda url: json.dumps(feed).encode())
        self.assertEqual([e['kind'] for e in result['events']], ['reopened'])
        self.assertEqual(result['review_queue'], [])
        self.assertEqual({r['family_key'] for r in self.load()['opportunities']}, {'synthetic:REF-shared'})

    def test_new_unlisted_rows_do_not_enter_review_queue(self):
        self.job['isListed'] = False
        result = self.refresh(apply=True)
        self.assertEqual(result['events'], [])
        self.assertEqual(result['review_queue'], [])
        self.assertEqual(self.load()['opportunities'], [])
        self.assertEqual(result['sources'][0]['suppressed'], 1)

    def test_malformed_semantic_fields_are_incomplete_not_silently_coerced(self):
        changes = [{'isRemote': 'false'}, {'isListed': 'false'}, {'descriptionPlain': {'bad': 'shape'}},
                   {'address': {'postalAddress': {'addressCountry': ['AT']}}},
                   {'secondaryLocations': ['Vienna']}, {'jobUrl': ''}, {'id': 'embedded whitespace'},
                   {'descriptionPlain': ''}]
        for change in changes:
            with self.subTest(change=change):
                self.save('opportunities.json', {'schema_version': 1, 'opportunities': []})
                self.payload = {'jobs': [dict(self.job, **change)]}
                try:
                    result = self.refresh(apply=True)
                except Exception as exc:
                    self.fail('bad row must be an incomplete source, not exception: ' + repr(exc))
                self.assertFalse(result['sources'][0]['complete'])
                self.assertEqual(self.load()['opportunities'], [])

    def test_historical_baseline_fills_observation_metadata_without_new_event(self):
        self.refresh(apply=True)
        registry = self.load()
        row = registry['opportunities'][0]
        row.update(fingerprint=None, decision='excluded', evidence=['/canonical/historical.md'])
        row.pop('published_at')
        self.save('opportunities.json', registry)
        self.job['publishedAt'] = '2020-01-02T00:00:00Z'
        result = self.refresh(apply=True)
        row = self.load()['opportunities'][0]
        self.assertEqual(result['events'], [])
        self.assertEqual(row.get('published_at'), '2020-01-02T00:00:00Z')
        self.assertEqual(row['first_seen'], '2026-11-13T12:00:00Z')
        self.assertIn('/canonical/historical.md', row['evidence'])
        self.assertTrue(any(str(self.workspace) in path for path in row['evidence']))
        self.assertEqual(row['country'], 'AT')

    def test_location_triage_does_not_treat_region_codes_or_us_vienna_as_austria(self):
        for country in ('Europe', 'EU', 'Global'):
            self.assertEqual(discovery.location_scope('Remote', country, True), 'location_review')
        for text, country in [('Vienna, VA', None), ('Vienna, Illinois', None), ('Vienna', 'CA')]:
            self.assertEqual(discovery.location_scope(text, country, True), 'out_of_scope')
        self.assertEqual(discovery.location_scope('Vienna, Austria', 'DE', True), 'location_review')
        self.assertEqual(discovery.location_scope('Berlin', 'DE', True), 'out_of_scope')


if __name__ == '__main__':
    unittest.main()

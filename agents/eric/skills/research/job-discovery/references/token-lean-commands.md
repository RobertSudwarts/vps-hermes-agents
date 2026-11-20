# Token-lean collection and inspection

Keep collection outputs in files; do not dump raw feeds or the entire register into the conversation. The helper performs no model inference. Its stdout is JSON and can include a sizeable unresolved-key backlog, so redirect it before examining a compact summary.

```bash
HELPER=/opt/data/profiles/eric/skills/research/job-discovery/scripts/discovery.py
WORKSPACE=/vault/eric/Research/job-search
python3 -B "$HELPER" refresh --workspace "$WORKSPACE" --apply \
  > "$WORKSPACE/verification/latest-refresh.json"
# Exit 1 means at least one partial/failed source: inspect it, do not hide it.
# Exit 2 is a command/schema/concurrency error; do not treat it as a valid run.
```

Use this compact inspector on the JSON report (the same code works on a saved `runs/.../report.json`):

```bash
python3 -B - "$WORKSPACE/verification/latest-refresh.json" <<'PY'
import json, sys
from collections import Counter
with open(sys.argv[1]) as stream:
    report = json.load(stream)
print(json.dumps({
    'events': dict(Counter(event['kind'] for event in report['events'])),
    'review_queue_count': len(report['review_queue']),
    'pending_review_count': len(report['backlog']),
    'sources': [{key: source.get(key) for key in
                 ('id', 'status', 'complete', 'count', 'errors')}
                for source in report['sources']],
    'report_path': report['report_path'],
}, indent=2))
PY
```

For candidate review, use code to join selected event/backlog keys to the register and emit only key, employer, title, location, location_scope, decision and existing reason first. Read full descriptions/primary pages selectively after that cheap screen. Do not use title keywords as irrevocable rejection rules; retain unusual work for human judgement.

A zero-event refresh is not proof that no suitable opportunities exist: an unresolved backlog may still deserve a bounded review, and the watchlist is not exhaustive. Distinguish those cases from genuinely new/changed observations. Broad search and parallel research should be deliberate rather than a default repeated after every refresh.

Never calculate the monetary bill from these mechanical counts or retrieval timings. Whole-conversation input, output, caching, model/provider pricing and any subsequent research are separate; only report usage measurements actually available.

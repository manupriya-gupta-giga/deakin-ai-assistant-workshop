"""Fictional campus event assistant. Offline, standard-library Python 3 only.
The decision function is a deterministic teaching stand-in, not an LLM.
Run: python3 demo.py
Run the intentionally broken selector: python3 demo.py --buggy
"""
import json
import sys

EVENTS = [
    {"id": "E1", "title": "Intro AI", "topic": "AI",
     "level": "beginner", "time": "Friday 16:00", "timezone": "Australia/Melbourne"},
    {"id": "E2", "title": "AI Project Studio", "topic": "AI",
     "level": "advanced", "time": "Friday 18:00", "timezone": "Australia/Melbourne"},
]

def decide(request, records, source_status="ok", buggy=False):
    if source_status != "ok":
        return {"status": "source_unavailable", "event_ids": []}
    required = {"id", "title", "topic", "level", "time", "timezone"}
    if any(not required.issubset(r) or
           any(not isinstance(r[k], str) or not r[k].strip() for k in required)
           for r in records):
        return {"status": "source_incomplete", "event_ids": []}
    seen = {}
    for r in records:
        if r["id"] in seen and seen[r["id"]] != r:
            return {"status": "source_conflict", "event_ids": []}
        seen[r["id"]] = r
    candidates = [
        r for r in seen.values()
        if r["topic"].casefold() == request["topic"].casefold()
        and (buggy or r["level"] == request["level"])
    ]
    if not candidates:
        return {"status": "no_match", "event_ids": []}
    if len(candidates) != 1 and not buggy:
        return {"status": "clarify", "event_ids": [r["id"] for r in candidates]}
    return {"status": "ready", "event_ids": [candidates[0]["id"]]}

def cases():
    req = {"topic": "AI", "level": "beginner"}
    advanced_first = [EVENTS[1], EVENTS[0]]
    missing = [{k: v for k, v in EVENTS[0].items() if k != "time"}]
    conflict = [EVENTS[0], dict(EVENTS[0], time="Friday 17:00")]
    ambiguous = [EVENTS[0], dict(EVENTS[0], id="E3", title="AI Starter Lab")]
    return [
        ("unique match", req, EVENTS, "ok", "ready", ["E1"]),
        ("no matching topic", dict(req, topic="biology"), EVENTS, "ok", "no_match", []),
        ("valid empty search", req, [], "ok", "no_match", []),
        ("missing source time", req, missing, "ok", "source_incomplete", []),
        ("conflicting records", req, conflict, "ok", "source_conflict", []),
        ("source timeout", req, EVENTS, "timeout", "source_unavailable", []),
        ("two beginner events", req, ambiguous, "ok", "clarify", ["E1", "E3"]),
        ("advanced event first", req, advanced_first, "ok", "ready", ["E1"]),
    ]

def run(buggy=False):
    failures = 0
    trace = []
    for name, request, records, state, expected_status, expected_ids in cases():
        observed = decide(request, records, source_status=state, buggy=buggy)
        passed = (observed["status"] == expected_status
                  and observed["event_ids"] == expected_ids)
        failures += not passed
        print(f'{"PASS" if passed else "FAIL"}  {name}: {observed}')
        trace.append({"case": name, "request": request, "source_status": state,
                      "source_records": records, "observed": observed,
                      "expected": {"status": expected_status, "event_ids": expected_ids},
                      "passed": passed})
    print(f"\n{len(trace)-failures}/{len(trace)} fictional cases passed.")
    return failures, trace

if __name__ == "__main__":
    buggy = "--buggy" in sys.argv
    failures, trace = run(buggy)
    if "--json" in sys.argv:
        print(json.dumps(trace, indent=2))
    # A nonzero status is intentional for the broken demonstration.
    sys.exit(1 if failures else 0)


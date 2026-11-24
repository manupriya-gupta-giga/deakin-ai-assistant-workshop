"""Additional cases for discussion. Run python3 exercises.py."""
from demo import decide, EVENTS
request = {"topic": "AI", "level": "beginner"}
cases = [
    ("lowercase topic", dict(request, topic="ai"), EVENTS, "ready", ["E1"]),
    ("identical duplicate", request, [EVENTS[0], EVENTS[0]], "ready", ["E1"]),
    ("empty time", request, [dict(EVENTS[0], time="")], "source_incomplete", []),
]
for name, req, records, status, ids in cases:
    result = decide(req, records)
    assert result == {"status": status, "event_ids": ids}, (name, result)
    print("PASS", name, result)

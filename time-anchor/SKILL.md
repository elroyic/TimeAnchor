---
name: time-anchor
description: Offload date math to code — get current date, days/weeks until goal dates, and month-end info. Use whenever you need to reason about relative dates or calculate "how many days until [event]." Especially important when comparing milestone timelines against today's date. Triggers on any message mentioning dates, deadlines, timeframes, "when," "days until," planning, scheduling, or temporal reasoning.
---

# Time Anchor

Use `exec` to run the bundled script instead of doing date math yourself. The script returns deterministic results — no guessing.

## When to Use This Skill

- Any message mentioning dates, deadlines, timeframes ("in June," "next week," "by August")
- Comparing multiple milestone timelines against today
- Calculating how many days/weeks remain until an event
- Responding with temporal context (e.g., "today is X, that's Y weeks away from Z")

## Usage

```bash
python3 ~/.openclaw/workspace/skills/time-anchor/scripts/time-anchor.py [--today | --days NAME | --weeks NAME | --month]
# Omit flags for full anchor output
```

### Available Flags

| Flag | Output |
|------|--------|
| (none) | Full anchor: today, day of week, all goals in days/weeks, month info |
| `--today` | Today's date and day of week only |
| `--days NAME` | Days until specific goal |
| `--weeks NAME` | Weeks until specific goal |
| `--month` | Days left in current month (excluding today) |

### Configured Goals

Add/remove goals by editing the script or calling with custom dates:

- `plaster-cure-end` → 2026-06-01 (earliest painting window)
- `spaceX-ipo-listing` → 2026-06-15 (mid-June target, ~2 weeks after roadshow starts)
- `sasol-q2-results` → 2026-08-01 (Q2 results expected)

### Example Workflow

User: "When should I check if the plaster is ready?"
→ Run `time-anchor.py --days plaster-cure-end`
→ Script returns exact days remaining
→ Reply with concrete timeframe, not vague ranges like "a couple weeks"

## Adding New Goals

Edit `~/.openclaw/workspace/skills/time-anchor/scripts/time-anchor.py`, add to the `GOALS` dict:

```python
GOALS = {
    "new-goal-name": (2026, 7, 15),  # YYYY, MM, DD
}
```

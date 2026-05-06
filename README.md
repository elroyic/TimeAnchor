# Time Anchor 🔗

Deterministic date math for AI agents. No guessing, no mental calendar arithmetic, no context-churn drift.

## Why This Exists

LLMs are catastrophically bad at date math. Even when an LLM "knows" today's date, a few turns of conversation push the anchor further back in token weight until responses become inconsistent — sometimes saying "May has 30 days," other times getting weekday offsets wrong entirely.

This script offloads all date calculations to code. You pass it a date or weekday name and get exact results every time.

## Quick Start

```bash
# Full anchor: today + all configured goals
python3 time-anchor/scripts/time-anchor.py

# Just today
python3 time-anchor/scripts/time-anchor.py --today

# Specific date
python3 time-anchor/scripts/time-anchor.py --until 2026-12-25

# Weekday lookup (returns next occurrences, flags ambiguity)
python3 time-anchor/scripts/time-anchor.py --weekday Tuesday

# Month info
python3 time-anchor/scripts/time-anchor.py --month
```

## Ambiguity Detection

This is where time-anchor differs from everything else. When you ask "how far until Tuesday?" on a Wednesday, there are two Tuesdays within 14 days — the tool returns **both** with an `ambiguous: true` flag and structured JSON so the agent knows to ask for clarification instead of guessing.

```bash
$ python3 time-anchor/scripts/time-anchor.py --weekday Tuesday
Upcoming Tuesdays:
  this Tuesday (2026-05-12) -> +6 days / 0.9 weeks
  next Tuesday (2026-05-19) -> +13 days / 1.9 weeks
{"ambiguous": true, "options": [
  {"date": "2026-05-12", "label": "this_week", "days_until": 6},
  {"date": "2026-05-19", "label": "next_week", "days_until": 13}
]}
```

## Configured Goals

Edit the `TARGETS` dict in `time-anchor/scripts/time-anchor.py`:

```python
TARGETS = {
    "2026-06-01": "Plaster painting window",
    "2026-06-15": "SpaceX IPO listing",
    "2026-08-01": "Sasol Q2 results",
}
```

Run `time-anchor.py` with no flags to see all configured goals and their distance from today.

## Workflow Rules (for agents using this skill)

1. **Named event?** Check configured targets → check memory/context → web search → ask. Never guess a date.
2. **Weekday reference?** Default to the next upcoming occurrence (forward-looking).
3. **Past-tense phrasing** ("last Tuesday," "since summer started")? Look backward at most recent occurrence.
4. **Ambiguity flagged by `--weekday`?** Ask for clarification. Don't pick one.

## Install via ClawHub

```bash
openclaw skills install elroyic/TimeAnchor
```

## License

MIT — do whatever you want with it. It's a 200-line Python script that saves you from saying "let me check the calendar" every five minutes.

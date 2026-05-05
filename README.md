# Time Anchor ⏱️

**Deterministic date math for AI agents — never do calendar arithmetic in your head again.**

A lightweight OpenClaw skill that offloads all date calculations to code. Returns exact days, weeks, and month-end info for any arbitrary target date. No guessing, no mental math, no "May has 30 days" errors.

---

## Why

LLMs are terrible at date math even when they know today's date. Context churn pushes the anchor further back in token weight, leading to inconsistent responses across a single conversation. Time Anchor solves this by making all date calculations deterministic via code.

## Features

- **Arbitrary dates** — `--until YYYY-MM-DD` works with any target (no pre-registration needed)
- **Configured targets** — Pre-set milestones for recurring checks
- **Month info** — Days remaining in current month, excluding today
- **Today check** — Date and day of week
- **Full anchor** — All configured targets + month info at a glance

## Installation

### Via ClawHub (recommended)

```bash
openclaw skills install elroyic/TimeAnchor
```

Or search for it on [ClawHub](https://clawhub.ai).

### Manual Install

1. Clone or copy `time-anchor/` into your OpenClaw skills directory:
   ```bash
   cp -r time-anchor ~/.openclaw/skills/time-anchor
   ```

2. Ensure Python 3 is available (the script requires only standard library modules — no pip dependencies).

## Usage

### Quick checks

```bash
# Today's date and day of week
python3 skills/time-anchor/scripts/time-anchor.py --today
→ 2026-05-05 (Tuesday)

# Days left in current month (excluding today)
python3 skills/time-anchor/scripts/time-anchor.py --month
→ May 2026: 26 days remaining
```

### Arbitrary dates (primary interface)

```bash
# Any target date, no pre-registration needed
python3 skills/time-anchor/scripts/time-anchor.py --until 2026-10-15
→ Target: 2026-10-15 | From: 2026-05-05 (Tuesday) | +163 days / 23.3 weeks in

# Past dates work too
python3 skills/time-anchor/scripts/time-anchor.py --until 2026-02-28
→ Target: 2026-02-28 | From: 2026-05-05 (Tuesday) | -66 days / -9.4 weeks ago
```

### Full anchor (all configured targets + today)

```bash
python3 skills/time-anchor/scripts/time-anchor.py
→ Today: 2026-05-05 (Tuesday)
→ End of May             (2026-05-31) → +26 days / 3.7 weeks in
→ Plaster painting window(2026-06-01) → +27 days / 3.9 weeks in
→ SpaceX IPO listing     (2026-06-15) → +41 days / 5.9 weeks in
→ Sasol Q2 results       (2026-08-01) → +88 days / 12.6 weeks in
```

## Adding Custom Targets

Edit the `TARGETS` dict in `scripts/time-anchor.py`:

```python
TARGETS = {
    "2026-05-31": "End of May",
    "2026-06-01": "Plaster painting window",
    # Add your own:
    "2026-07-04": "Independence Day",
}
```

Or skip pre-registration entirely — use `--until` for one-off dates.

## License

MIT © 2026 [elroyic](https://github.com/elroyic)

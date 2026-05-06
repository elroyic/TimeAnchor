#!/usr/bin/env python3
"""Time anchor - deterministic date math for any target date."""

import json
import sys
from datetime import datetime, timedelta


# --- Defaults: convenience targets (not required; --until is primary) ---
TARGETS = {
    "2026-05-31": "End of May",
    "2026-06-01": "Plaster painting window",
    "2026-06-15": "SpaceX IPO listing",
    "2026-08-01": "Sasol Q2 results",
    # Add named events as they come up: "YYYY-MM-DD": "Event name"
}

# --- Weekday name to 0=Monday, 6=Sunday mapping ---
DAY_MAP = {name: idx for idx, name in enumerate(
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
)}


def validate_date(date_str):
    """Validate and normalize a date string to YYYY-MM-DD."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d"), dt
    except ValueError:
        print(
            f"Error: Invalid date format '{date_str}'. Expected YYYY-MM-DD.",
            file=sys.stderr,
        )
        sys.exit(1)


def today():
    """Return today's date string and datetime object."""
    now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    return now.strftime("%Y-%m-%d"), now


def days_between(date_str_from, date_str_to):
    """Calculate days between two YYYY-MM-DD dates."""
    _, d1 = validate_date(date_str_from)
    _, d2 = validate_date(date_str_to)
    delta = (d2 - d1).days
    weeks = round(delta / 7, 1) if delta >= 0 else -(round(abs(delta) / 7, 1))
    return delta, weeks


def resolve_weekday(name):
    """Resolve a weekday name to canonical capitalization and index.

    Supports: 'Tuesday', 'tuesday', 'tue' (fuzzy), etc.
    Returns (canonical_name, day_index) or exits on error.
    """
    day_lower = name.strip().lower()

    # Exact case-insensitive match
    exact = [k for k in DAY_MAP if k.lower() == day_lower]
    if len(exact) == 1:
        return exact[0], DAY_MAP[exact[0]]
    if len(exact) > 1:
        print(
            f'Error: Multiple weekday matches for "{name}". '
            f"Options: {', '.join(DAY_MAP.keys())}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Fuzzy first-4-letter match (e.g. "tue" -> Tuesday)
    fuzzy = [k for k in DAY_MAP if k.lower().startswith(day_lower)]
    if len(fuzzy) == 1:
        return fuzzy[0], DAY_MAP[fuzzy[0]]

    print(
        f'Error: Unknown weekday "{name}". Options: {", ".join(DAY_MAP.keys())}',
        file=sys.stderr,
    )
    sys.exit(1)


def weekday_targets(name):
    """Find all upcoming occurrences of a named weekday.

    Returns human-readable lines + JSON on the last line for programmatic use.

    When multiple Tuesdays fall within 7 days, flags AMBIGUOUS and provides both
    options so the agent can ask for clarification instead of guessing.

    Usage: time-anchor.py --weekday Tuesday
           time-anchor.py --weekday tue   (fuzzy match)
    """
    day_name, target_day_idx = resolve_weekday(name)
    _, now = today()

    # Collect future occurrences (up to 3 weeks ahead, max 2 results)
    future = []
    for offset in range(0, 22):
        candidate = now + timedelta(days=offset)
        if candidate.weekday() == target_day_idx:
            future.append(candidate.strftime("%Y-%m-%d"))
            if len(future) >= 2:
                break

    # If only one result and it's >7 days away, no ambiguity.
    # If two results within ~14 days, there's a "this week" vs "next week" issue.
    is_ambiguous = False
    if len(future) >= 2:
        d0 = datetime.strptime(future[0], "%Y-%m-%d")
        d1 = datetime.strptime(future[1], "%Y-%m-%d")
        is_ambiguous = (d1 - d0).days <= 14

    print(f'Upcoming {day_name}s:')
    for d_str in future:
        delta, weeks = days_between(today()[0], d_str)
        marker = "" if delta != 0 else " <- TODAY"
        label = f"this {day_name}" if delta <= 7 else f"next {day_name}"
        print(f"  {label} ({d_str}) -> {delta:+d} days / {weeks:.1f} weeks{marker}")

    # JSON payload for agent-level disambiguation
    options = []
    for d_str in future:
        delta, _ = days_between(today()[0], d_str)
        label_key = "this_week" if delta <= 7 else "next_week"
        options.append(
            {"date": d_str, "label": label_key, "days_until": delta}
        )

    result_json = {"ambiguous": is_ambiguous, "options": options}
    print(json.dumps(result_json))


def full_anchor():
    """Run full anchor: today + all configured targets."""
    today_str, now = today()

    lines = [f"Today: {today_str} ({now.strftime('%A')})"]
    lines.append("")

    for target_date, label in TARGETS.items():
        delta, weeks = days_between(today_str, target_date)
        direction = "in" if delta >= 0 else ""
        lines.append(
            f"{label:35s} ({target_date}) -> {delta:+d} days / {weeks} weeks {direction}"
        )

    # Month info
    _, now_raw = today()
    month_end = (datetime(now_raw.year, now_raw.month + 1, 1) - timedelta(days=1))
    days_left = (month_end - now_raw).days
    lines.append("")
    lines.append(
        f"{now_raw.strftime('%B')} {now_raw.year}: "
        f"{days_left} days remaining (excluding today)"
    )

    return "\n".join(lines), full_anchor_json(today_str)


def full_anchor_json(today_str):
    """Return structured JSON for programmatic use."""
    result = {"today": today_str, "targets": {}, "month_info": {}}
    now_dt = datetime.strptime(today_str, "%Y-%m-%d")

    for target_date, label in TARGETS.items():
        delta, weeks = days_between(today_str, target_date)
        result["targets"][target_date] = {
            "label": label,
            "days_until": delta,
            "weeks_until": weeks,
        }

    month_end = (datetime(now_dt.year, now_dt.month + 1, 1) - timedelta(days=1))
    days_left = (month_end - now_dt).days
    result["month_info"] = {
        "current_month": now_dt.strftime("%B %Y"),
        "days_remaining_excluding_today": days_left,
    }

    return json.dumps(result, indent=2)


def single_target(target_str):
    """Calculate days until a specific arbitrary date."""
    target_str, td = validate_date(target_str)
    today_str, _ = today()
    delta, weeks = days_between(today_str, target_str)
    direction = "in" if delta >= 0 else ""

    print(f"Target: {target_str}")
    print(
        f"From:   {today_str} ({datetime.strptime(today_str, '%Y-%m-%d').strftime('%A')})"
    )
    print(f"Days:   {delta:+d} days / {weeks} weeks {direction}")


if __name__ == "__main__":
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        help()
        sys.exit(0)

    if "--weekday" in args:
        idx = args.index("--weekday")
        target_str = args[idx + 1] if idx + 1 < len(args) else None
        if not target_str:
            print(
                "Error: --weekday requires a weekday name (e.g., Tuesday)",
                file=sys.stderr,
            )
            sys.exit(1)
        weekday_targets(target_str)

    elif "--until" in args:
        idx = args.index("--until")
        target_str = args[idx + 1] if idx + 1 < len(args) else None
        if not target_str:
            print(
                "Error: --until requires a date argument (YYYY-MM-DD)", file=sys.stderr
            )
            sys.exit(1)
        single_target(target_str)

    elif "--month" in args:
        _, now_raw = today()
        month_end = (datetime(now_raw.year, now_raw.month + 1, 1) - timedelta(days=1))
        days_left = (month_end - now_raw).days
        print(
            f"{now_raw.strftime('%B')} {now_raw.year}: "
            f"{days_left} days remaining (excluding today)"
        )

    elif "--today" in args:
        today_str, now = today()
        print(f"{today_str} ({now.strftime('%A')})")

    else:
        output, _ = full_anchor()
        print(output)

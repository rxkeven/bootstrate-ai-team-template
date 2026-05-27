# Skill: Loop SOP

Defines the three canonical loop types and their operating patterns. Referenced in role boot prompts.

## Session types: on-demand vs per-task vs CEO-bottleneck

**Per-task (valid):** PM dispatches a specific task brief to the role's inbox. The role activates, processes the brief, delivers output to PM's inbox, and ends. Example: Designer activated for a sprint, produces specs, sends to PM, ends.

**Scheduled loop (preferred for recurring-work roles):** Role runs on a scheduled cadence. Checks inbox autonomously without {CEO_ROLE} or PM triggering a session. Example: HR Manager on work-driven Cowork loop.

**CEO-bottleneck (anti-pattern -- avoid unless justified):** {CEO_ROLE} must manually open a session for the role to receive any work. Acceptable only for genuinely infrequent specialist roles. Requires explicit {CEO_ROLE} sign-off with documented reason.

When in doubt: if a role will receive recurring work from PM, it needs a loop.

## Loop types

### Fixed-interval
- Runs on a cron schedule regardless of work state
- Most common: `*/30 * * * *`
- Example roles: `pa-cowork`, `pm`
- Scheduled wake-ups: yes

### Fixed-interval (adaptive)
- Runs at a base cadence but adjusts based on queue depth (e.g. 15 min when active, 30 min when quiet)
- Example roles: `coordinator`
- Scheduled wake-ups: yes

### Work-driven
- Loops at 30-min cadence while tasks are open or replies are pending
- When all-clear: schedule next check 7AM next business day
- Example roles: `hr-manager`, `engineer`
- Scheduled wake-ups: yes

### Work-driven (Cowork)
- Self-scheduled Cowork monitor; work-driven by active reports and on-demand requests
- Example roles: `portfolio-manager`
- Scheduled wake-ups: yes (cron-based Cowork session)

### On-demand
- No scheduled loop. Session activates when {CEO_ROLE} or PM manually starts it
- Valid for infrequent specialist work
- Example roles: `designer`, `strategist`, `ccs`, `board`
- Note: if a role becomes recurring-work, evaluate switching to work-driven

## Start-of-loop date check

Run at the start of every loop tick before any other work:

```bash
date -u +'%Y-%m-%dT%H:%M:%SZ'
date '+%H:%M %A %Z'
```

Capture both outputs. Include the local date in your loop report `Today:` line. This anchors every loop report to a verifiable day-of-week + timestamp and prevents context drift during long sessions.

## Loop report

Every Cowork role produces a structured loop report at end of each cycle. Format defined in role boot prompt. Minimum fields:

- **Today:** {DoW YYYY-MM-DD HH:MM local (UTC ISO)} — sourced from the start-of-loop date check
- timestamp
- role identifier
- what was processed
- current status
- next scheduled wake-up

Loop reports go to PM inbox (or {CEO_ROLE} inbox for CEO-reporting roles).

## Business hours

Default: 7AM to 7PM local time. Active loops: 30-min interval. Outside business hours: schedule 7AM next business day.

## Change log

- 2026-05-27 v1.1 — Added start-of-loop date check section and Today: minimum field to loop report. Added Fixed-interval (adaptive) and Work-driven (Cowork) loop types. Phase 1 Item 7.

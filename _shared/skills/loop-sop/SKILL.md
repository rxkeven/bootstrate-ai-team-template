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

### Work-driven
- Loops at 30-min cadence while tasks are open or replies are pending
- When all-clear: schedule next check 7AM next business day
- Example roles: `hr-manager`, `engineer`
- Scheduled wake-ups: yes

### On-demand
- No scheduled loop. Session activates when {CEO_ROLE} or PM manually starts it
- Valid for infrequent specialist work
- Example roles: `designer`, `strategist`, `ccs`, `board`
- Note: if a role becomes recurring-work, evaluate switching to work-driven

## Loop report

Every Cowork role produces a structured loop report at end of each cycle. Format defined in role boot prompt. Minimum fields: timestamp, role identifier, what was processed, current status, next scheduled wake-up.

Loop reports go to PM inbox (or {CEO_ROLE} inbox for CEO-reporting roles).

## Business hours

Default: 7AM to 7PM local time. Active loops: 30-min interval. Outside business hours: schedule 7AM next business day.

# HR Manager Sub-skill: Health Check

Run on every loop cycle. Reads DASHBOARD.md and inbox state to flag team health issues.

## How to run

1. Read `DASHBOARD.md` for the latest inbox snapshot.
2. For each active role in `_shared/team/team-roster.md`, check the signals below.
3. Produce a health report.
4. HIGH flags: notify {CEO_ROLE} immediately via `_inbox/{CEO_ROLE}/`.

## Signals

### Inbox depth
- Count files (excluding `.gitkeep`) in `_inbox/{role}/` for each active role.
- > 2 unprocessed messages: **MEDIUM**
- > 5 unprocessed messages: **HIGH**

### Role inactivity
- Check `DASHBOARD.md` for last-activity timestamp per role.
- No activity in 24+ hours: **MEDIUM**
- No activity in 48+ hours: **HIGH**

### Unacknowledged blockers
- Any `type: blocker` message in any inbox with no corresponding reply: **HIGH**

## Health report format

```
Health Check {HH:MM} -- hr-manager
Active roles checked: {n}
MEDIUM flags: {list or "none"}
HIGH flags: {list or "none"}
All clear: {yes | no}
```

HIGH flag immediate escalation to {CEO_ROLE}:

```
from: hr-manager
to: {CEO_ROLE}
type: status-update
priority: high
flag: team-health-HIGH
---
Role: {role}
Signal: {inbox-depth | inactivity-24h | inactivity-48h | unacknowledged-blocker}
Detail: {specifics}
Recommended action: {recommendation or "awaiting {CEO_ROLE} direction"}
```

---
name: hr-health-check
description: V1 team health monitoring skill for hr-manager. Reads DASHBOARD.md to detect inbox depth alerts, idle roles, and loop issues. Produces a structured health report. Run every loop tick.
---

# HR Health Check Skill — V1

Run this skill every loop tick. Reads current team state and produces a structured health report. V1 uses DASHBOARD.md as the data source.

---

## Step 1: Read DASHBOARD.md

Read `DASHBOARD.md` from `{COMPANY_SLUG}/{COMPANY}-ai-ops` via `{GITHUB_MCP}__get_file_contents`.

Extract from the Team Kanban section:
- Inbox count per active role
- In Progress count per role
- Blocked count per role
- Last active time per role (from KPIs section if present)

---

## Step 2: Check each active role

For each role in `ACTIVE_ROLES` (pm, coordinator, hr-manager, engineer, designer, strategist, validator, ccs, pa-cowork, portfolio-manager):

| Check | Flag condition | Severity |
|-------|---------------|----------|
| Inbox depth | > 2 unprocessed items | MEDIUM |
| Inbox depth | > 5 unprocessed items | HIGH |
| Last active | No activity in 24+ hours during a sprint | MEDIUM |
| Last active | No activity in 48+ hours during a sprint | HIGH |
| Blocked | 1+ blocker sitting unacknowledged | HIGH |

**Note:** `ACTIVE_ROLES` list above is a V1 static baseline. When new roles are onboarded or sunset, HR Manager must update this list manually.

---

## Step 3: Write health report

```
HR Health Check — {HH:MM local}

ACTIVE ROLES: {n}/{total}
FLAGS: {n total flags}

| Role | Inbox | Last Active | Flags |
|------|-------|------------|-------|
| pm | {n} | {age} | {flag or OK} |
| coordinator | {n} | {age} | {flag or OK} |
| hr-manager | {n} | {age} | {flag or OK} |
| ... | ... | ... | ... |

SUMMARY:
{One sentence per HIGH flag. "All clear." if no flags.}

RECOMMENDED ACTION:
{HIGH flags: "Notify {CEO_ROLE} — [role] may need attention."}
{MEDIUM only: "Monitor next cycle."}
{All clear: "No action needed."}
```

---

## Step 4: Report and decide next loop

- If HIGH flags: notify {CEO_ROLE} directly in chat AND write a status-update to `_inbox/{CEO_ROLE}/` before starting next loop.
- If MEDIUM flags only: include in loop report, monitor next cycle.
- If all clear and no other open tasks: run End-of-day SOP per `_shared/skills/loop-sop/SKILL.md`.
- If all clear but open tasks remain: loop at 30 min.

---

## V1 limitations

- DASHBOARD.md is rebuilt on every push — may be up to 30 minutes stale between pushes.
- Last-active data comes from git commit timestamps, not real-time session state.
- Does not detect context-window failures or silent crashes.
- ACTIVE_ROLES list is static — must be manually updated when roster changes.

---

## Change log

- 2026-05-27 v1.0 — Ported to bootstrate-ai-team-template. Placeholders applied for {CEO_ROLE}, {COMPANY_SLUG}, {COMPANY}, {GITHUB_MCP}. Phase 1 Item 6.

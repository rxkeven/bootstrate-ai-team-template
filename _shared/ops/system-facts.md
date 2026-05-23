# System Facts

Canonical configuration file. Read on session start by all roles that reference it. Populated by the operator after scaffold, before activating any agents.

## GitHub

| Key | Value |
|---|---|
| GitHub org / owner | `{TARGET_OWNER}` |
| Ops repo | `{TARGET_OWNER}/{TARGET_REPO}` |
| MCP connection name | `mcp__github__` |

## Team identity

| Key | Value |
|---|---|
| Company name | `{COMPANY}` |
| Consumer brand | `{BRAND}` |
| CEO role identifier | `{CEO_ROLE}` |

## Content rules

| Key | Value |
|---|---|
| Em-dash rule | `{HOUSE_STYLE_EM_DASH}` |

## Surfaces reference

Canonical surface for each standard role. `team-roster.md` is authoritative for the active team; this table is a quick lookup for new role sessions.

| Role | Identifier | Default surface |
|---|---|---|
| HR Manager | `hr-manager` | Claude Code Desktop |
| Project Manager | `pm` | Claude Cowork |
| Engineer | `engineer` | Claude Code |
| Designer | `designer` | Claude Chat |
| Strategist | `strategist` | Claude Chat |
| Validator | `validator` | Claude Console Managed Agent |
| Client Care Specialist | `ccs` | Claude Chat |
| Board / Advisor | `board` | Claude Chat |
| Personal Assistant | `pa-cowork` | Claude Cowork |

## Notes

- Populate all values above before activating any agent. HR Manager reads this file on first cycle.
- If a role will run on a different surface than the default, update both this table and `team-roster.md` before activating.
- Do not let this file drift from `team-roster.md`. `team-roster.md` is authoritative; this file is for quick lookup.

# {COMPANY} AI Team Roster

Canonical list of all roles in the {COMPANY} AI team, their status, surfaces, and the manager they report to. Update this file whenever a role is added, retired, or changes surface (HR Manager skill).

## Active roles

| Role | Identifier | Surface | Reports to | Status | Started |
|---|---|---|---|---|---|
| HR Manager | `hr-manager` | Claude Code Desktop | {CEO_ROLE} | Active | {DATE} |
| Project Manager | `pm` | Claude Cowork | {CEO_ROLE} | Active | {DATE} |
| Engineer | `engineer` | Claude Code | pm | Active | {DATE} |
| Designer | `designer` | Claude Chat | pm | Active (on-demand) | {DATE} |
| Strategist | `strategist` | Claude Chat | {CEO_ROLE} | Active (on-demand) | {DATE} |
| Validator | `validator` | Console Managed Agent | pm | Active (per-checkpoint) | {DATE} |
| Client Care Specialist | `ccs` | Claude Chat | {CEO_ROLE} | Active | {DATE} |
| Board / Advisor | `board` | Claude Chat | N/A | Active (weekly) | {DATE} |
| Personal Assistant | `pa-cowork` | Claude Cowork | {CEO_ROLE} | Active | {DATE} |

## Retired roles

| Role | Identifier | Retired | Reason |
|---|---|---|---|
| (none yet) | | | |

## Status definitions

- **Active:** Standing session running continuously or on a scheduled loop
- **Active (on-demand):** Role exists, session activates per request
- **Active (per-checkpoint):** Activates on a scheduled checkpoint trigger
- **Active (weekly):** Engaged at a weekly cadence
- **Retired:** No longer active. Files retained for reference.
- **In training:** Configured but not yet operational

## Change log

| Date | Change | Authorized by |
|---|---|---|
| {DATE} | Initial roster established via ai-team-bootstrap V1.0 | {CEO_ROLE} |
| {DATE} | HR Manager added as standard built-in role (V1.1.5) | {CEO_ROLE} |
| 2026-05-23 | hr-manager surface corrected: Claude Cowork → Claude Code Desktop (Item 3) | bs-code-eng |

## Notes

- Each row corresponds to a role definition at `_shared/team/roles/{identifier}.md` and a boot prompt at `_shared/team/role-prompts/{identifier}.md`.
- For multi-engineer setups, append project slug to the engineer identifier (e.g., `engineer-platform`).
- HR Manager skill at `_shared/skills/hr-manager/SKILL.md` is the entry point for any roster change.

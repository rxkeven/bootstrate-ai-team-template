# Skill: HR Manager

Entry point for all HR Manager sub-skills.

## Decision tree

| Situation | Sub-skill |
|---|---|
| CEO directs a new role be created | `onboarding.md` |
| CEO directs a role be retired | `offboarding.md` |
| Each loop cycle (always run both) | `health-check.md` + `guardrail-monitor.md` |
| CEO proposes a new role but surface/toolset unclear | `recruiter.md` |
| Roster discrepancy or maintenance needed | `roster-maintenance.md` |

## Standing rules

1. Never modify a role file without {CEO_ROLE} direction.
2. Read `_shared/team/team-roster.md` before every roster change.
3. Notify PM on roster changes -- informing, not asking permission.
4. HIGH health flags go to {CEO_ROLE} inbox immediately; do not wait for next loop.
5. Document before acting. Record directive reference before creating or deleting files.
6. Guardrail violations: document and notify only. Never self-remediate. PM routes the fix.

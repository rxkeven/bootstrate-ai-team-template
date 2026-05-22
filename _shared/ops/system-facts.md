# System Facts

Canonical instance configuration. Read on every session start before doing anything else. The operator fills this in at scaffold time.

## GitHub

| Item | Value |
|------|-------|
| GitHub org / owner | `{GITHUB_OWNER}` |
| Ops repo | `{GITHUB_OWNER}/{TARGET_REPO}` |
| Code repo(s) | `{REPO_URL}` |
| MCP connection name | `{MCP_CONNECTION_NAME}` |

> The MCP connection name is what you pass to tools requiring a named connection. All agents use the same fine-grained PAT scoped to the repos above.

## Identity

| Item | Value |
|------|-------|
| Company / project name | `{COMPANY}` |
| CEO role identifier | `{CEO_ROLE}` |
| Brand name (external) | `{BRAND}` |
| Em-dash house rule | `{HOUSE_STYLE_EM_DASH}` |

## Roles and surfaces (summary)

Full canonical roster: `_shared/team/team-roster.md`.

| Role | Identifier | Surface |
|------|------------|--------|
| CEO | `{CEO_ROLE}` | All |
| Project Manager | `pm` | Claude Cowork |
| Personal Assistant | `pa-cowork` | Claude Cowork |
| (add roles at scaffold time) | | |

## Instance notes

*Operator: add any instance-specific facts here — timezone, active projects, key external integrations, environment-specific constraints.*

# MCP Availability Matrix

Which MCP tools and surface-level capabilities each role has access to. Use this when planning work that depends on a specific tool, or when deciding which surface to use for a new role.

Last updated: {DATE}.

## By surface

| Capability | Claude Code | Claude Cowork | Claude Chat | Console Managed Agent | Custom (Hermes etc.) |
|---|---|---|---|---|---|
| GitHub MCP | Yes | Yes | Yes (via Desktop) | Yes (configured) | Custom integration |
| Database MCPs (Supabase, etc.) | Yes | Limited | Yes (via Desktop) | Read-only typical | Per config |
| Deploy MCPs (Vercel, etc.) | Yes | No | Yes (via Desktop) | No | Per config |
| Workflow MCPs (n8n, Make, Zapier) | Yes | Yes | Yes (via Desktop) | No | Per config |
| Asset gen MCPs (Higgsfield etc.) | No | No | Yes (via Desktop) | No | No |
| Data MCPs (Airtable, Notion) | Yes | Yes | Yes (via Desktop) | No | Per config |
| Bash / local filesystem | Yes | No | No | No | Per config |
| Scheduled tasks | No | Yes | No | Managed externally | Per config |
| Web search | Yes | Yes | Yes | Limited | No |
| File creation / mount | Yes (`/mnt/user-data/`) | No | Yes (artifacts) | No | Per config |
| Notification channels (iMessage etc.) | No | No | No | No | Yes (per role) |

## By role (default for {COMPANY})

| Role | Surface | Primary MCPs needed |
|---|---|---|
| `pm` | Claude Cowork | GitHub, scheduled tasks |
| `pa-cowork` | Claude Cowork | GitHub, scheduled tasks |
| `engineer` (per project) | Claude Code | GitHub, project-specific (database, deploy, workflow), bash |
| `designer` | Claude Chat | GitHub, asset gen if applicable |
| `strategist` | Claude Chat | GitHub |
| `validator` | Console Managed Agent | GitHub |
| `ccs` | Claude Chat | GitHub |
| `board` | Claude Chat | None required |

## Implications

- **Cowork agents cannot run bash.** PM and PA must use GitHub MCP for everything, including "list a directory." There is no `ls`; use `get_file_contents` against the directory path.
- **Code agents own the heavy lifting on infra.** Migrations, deploys, smoke tests, log capture all happen in Claude Code sessions for Engineers.
- **Chat is the most tool-flexible surface** but lacks scheduled execution. On-demand Chat roles work because their cadence is human-triggered.
- **Validator on Console Managed Agent** is intentionally constrained. The skill is review, not execution.

## When a role needs an MCP not on its surface

Two options:

1. **Route through a role that has it.** Example: Designer needs a database asset list. Route the ask through PM, PM routes to Engineer, Engineer queries the database and writes results to `_inbox/designer/`.
2. **Escalate to {CEO_ROLE} for a surface change.** If a role consistently needs a tool its surface does not provide, that is an HR-skill signal. Surface to {CEO_ROLE} via `decision-escalation` for a roster review.

## Out-of-scope notes

- Vault credentials never transit any MCP. Use vault item names only, per OpSec.
- The mcp-registry list_connectors tool reports installed connectors at runtime; this matrix is the planning reference, not the authoritative current state.

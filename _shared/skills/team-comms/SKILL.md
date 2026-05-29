---
name: team-comms
description: Standard communication protocol for all inter-agent messaging in the {COMPANY} AI team. Use at session start and before sending any message to another agent inbox.
---

# Team Communication Protocol

This is the canonical reference for how agents communicate. Every message between agents follows this protocol.

## Channel

All inter-agent communication happens via files in `_inbox/{role}/` directories in this repo. No direct chat-to-chat. No DMs. No verbal-only handoffs. Files are the audit trail.

## Filename convention

`_inbox/{to-role}/{ISO-timestamp-with-hyphens-for-colons}-{short-slug}.md`

- ISO timestamp uses hyphens instead of colons (filesystem-safe)
- Example: `2026-05-19T17-00-pm-shutdown-handoff.md`
- Same-second timestamps fall back to alphabetical sort, so use distinguishing slugs

## Frontmatter (required on every message)

```
---
from: {your-role}
to: {target-role}
project: {shared|project-slug}
type: task-brief | sprint-brief | status-update | decision-request | decision | handoff | context-handoff | blocker | validation-request | validation-result
priority: normal | high | urgent
kevin_required: false
decision_needed: false
references:
  - path/to/related-file
date: 2026-05-19T17:00:00Z
---
```

Field rules:

- `from` and `to`: role identifiers, never human names
- `project`: `shared` for cross-project, else the project slug
- `type`: pick one from the list; if none fits, default to `status-update`
- `priority`: `normal` unless time-bounded
- `kevin_required`: true only if the CEO must personally see this
- `decision_needed`: true if the sender expects a binary or multi-option response
- `references`: relative paths to files that provide context

## Body structure

Markdown. Sections vary by `type`:

- **`task-brief` / `sprint-brief`:** acceptance criteria, scope, deadline, references to canonical specs
- **`status-update`:** current state, what is blocked, what is next
- **`decision-request`:** options surfaced, recommendation, what the sender will do if no response by a date
- **`handoff` / `context-handoff`:** state of the world, open queries, first-steps for receiver
- **`blocker`:** what is blocked, what would unblock it, urgency
- **`validation-request` / `validation-result`:** scope to validate, acceptance criteria, findings

Keep bodies under one screen when possible. Use references for longer context.

## Commit policy: batch by logical operation

Commit by logical operation, not per individual file action. Three commit groups:

1. **Inbox processing** — all archives, deletes, and state-marker updates for one inbox-processing flow → **1 commit**.
   Format: `{role}: process inbox — {summary}`
2. **Outgoing messages** — all messages sent as part of one logical flow → **1 commit**.
   Format: `msg: {from-role} -> {to-role}: {topic}` (comma-separate multiple recipients)
3. **Discrete decisions** — standalone scope, policy, or doc changes not tied to inbox processing → **1 commit each**.
   Format: `{role}: {decision-slug}`

Other conventions (apply at the logical-operation level):

- Decision logs: `decision: {project}: {summary}`
- Escalations: `escalation: {from-role} -> {ceo-role}: {topic}`

### Tool guidance

- Use `push_files` (not multiple single-file create/update calls) when creating or updating multiple files in the same logical operation. It commits them as one commit, eliminates fast-forward conflicts, and reduces log noise.
- File deletions cannot be batched — run them sequentially within the same logical operation.

## Routing rules

- All inter-role messages route through PM. Engineers do not message each other. Strategist does not message Engineers directly. Validator findings route through PM.
- The CEO inbox (`_inbox/{ceo-role}/`) is the escalation endpoint. Any role may write there when escalation criteria apply (see decision-escalation skill).
- PA Cowork is the only role that writes to multiple non-PM inboxes (relaying CEO replies).
- If you find a message in your inbox that should not be addressed to you, re-route it. Move the file to the correct inbox with a one-line note prepended to the body, as part of that inbox-processing commit.

## Response expectations

- `priority: urgent`: acknowledge within one cycle. If you cannot act immediately, send a brief status-update saying you have seen it and stating your ETA.
- `priority: high`: action or response within one working day
- `priority: normal`: action or response within the natural sprint cadence
- `decision_needed: true` and not actioned within priority window: surface to PM or CEO

## After writing a message

1. Verify the file landed (read it back if MCP showed any timeout pattern).
2. The recipient's scheduled monitor (Cowork) or next session start (Code/Chat) picks it up.
3. Move on. Do not poll for replies inside the same session.

## Edge cases

- **Reply to a specific message:** include the original filename in `references`. Frontmatter `type` is your own message type, not a "reply" type.
- **Two agents asking opposite things:** escalate to CEO via decision-escalation.
- **Message you cannot parse:** do not guess. Surface to the user and flag for fix in a `fix:` commit.
- **Sensitive content (financials, client identifiers, EINs):** do NOT put in the repo. Surface to CEO via chat, not via inbox.

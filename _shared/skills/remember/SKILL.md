---
name: remember
description: Canonical full-context-load skill. Loads universal skills, role definition, todo, current state, and recent handoffs. Single-shape — no variants. Invoked by preflight when work is found and context is stale or absent. Updates `_state/{role}/last-remember-utc.txt` on completion.
---

# /remember Skill

`/remember` is the canonical full-context-load for any role. Always loads everything — no variants.

---

## When this runs

1. **Auto by preflight** — when work is found and context is stale or absent
2. **Manual by {CEO_ROLE}** — `/remember` typed into chat to force full re-load
3. **Peer-initiated** — inbox message of `type: refresh-request` asking the role to refresh

---

## What /remember loads

In order:

### 1. Universal skills

Read in this order:
- `_shared/skills/loop-sop/SKILL.md`
- `_shared/skills/team-comms/SKILL.md`
- `_shared/skills/inbox-check/SKILL.md`
- `_shared/skills/decision-escalation/SKILL.md`
- `_shared/skills/context-discipline/SKILL.md`

### 2. Role definition

- `_shared/team/roles/{role}.md`

### 3. Role-specific state files

- `_todo/{role}.md`
- Any role-owned state files per role definition

### 4. Most recent handoff (session-start only)

- Read most recent non-.gitkeep .md in `_handoff/{role}/`
- If present: archive it to `_archive/_handoff/{role}/{YYYY-MM-DD}/` to confirm pickup

### 5. Team-wide reference (only if role definition requires)

- `_shared/team/team-roster.md` — for roles that route messages (pm, hr-manager)
- `DASHBOARD.md` — for roles that monitor team state (hr-manager)

### 6. Role-specific monitoring skills

If the role definition references one, load it now.

---

## After loading

1. Write current ISO timestamp to `_state/{role}/last-remember-utc.txt`. Format: single line, ISO-8601 UTC, no frontmatter. Example: `2026-05-27T07:00:00Z`.
2. Acknowledge in chat: "/remember complete — loaded {n} universal skills, role def, todo." (one line)
3. Hand control back to preflight (auto invocations) or to {CEO_ROLE} (manual invocations)

---

## State marker format

Plain ISO-8601 UTC timestamp on a single line. No frontmatter, no JSON.

```
2026-05-27T07:00:00Z
```

---

## Peer-initiated refresh

When another role wants you to refresh, they write to your inbox:

```yaml
---
from: {requester-role}
to: {your-role}
type: refresh-request
priority: normal
date: {ISO}
---

Please invoke /remember on your next inbox tick. Reason: {one line}.
```

When you pick up the message, invoke /remember immediately, then process the rest of the inbox normally.

---

## Failure modes

- **A required file is missing** → log to `_inbox/{CEO_ROLE}/` as `type: status-update` and continue with what loaded. Do not fabricate state.
- **`_state/{role}/last-remember-utc.txt` write fails** → still operate, but flag the failure so the next preflight tick treats context as stale and re-loads.

---

## Change log

- 2026-05-27 v1.0 — Ported to bootstrate-ai-team-template (Phase 1 sprint). Placeholders applied for CEO_ROLE.

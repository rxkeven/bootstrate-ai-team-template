# Handoff Protocols

Canonical reference for which role can communicate with which. Hub-and-spoke routing is permanent operating policy. Direct paths exist only where listed here.

## Routing matrix

| From → To | Allowed? | Channel |
|---|---|---|
| Any role → {CEO_ROLE} | Yes | `_inbox/{CEO_ROLE}/` for escalations |
| {CEO_ROLE} → Any role | Yes (via PA relay) | PA Cowork writes to target inbox |
| Any role ↔ PM | Yes | `_inbox/pm/` and `_inbox/{role}/` |
| Engineer ↔ Engineer | NO | Route through PM |
| Engineer ↔ Strategist | NO | Route through PM |
| Engineer ↔ Validator | NO | Route through PM |
| Engineer ↔ Designer | NO | Route through PM |
| Strategist ↔ Validator | NO | Route through PM |
| Strategist ↔ Designer | NO | Route through PM |
| Validator ↔ Designer | NO | Route through PM |
| CCS ↔ Engineers/Designer/Strategist/Validator | NO | Route through PM if engineering input needed, else through {CEO_ROLE} |
| Board ↔ Any role | NO | Board talks to {CEO_ROLE} only |
| PA Cowork ↔ Non-CEO roles | Relay only | PA only WRITES to other inboxes when relaying {CEO_ROLE}'s replies |

## Why the hub matters

A single hub through PM keeps the team coherent. Without it:

- Two Engineers can solve the same problem twice without coordination
- Validator findings can land on Engineers without disposition or prioritization
- Strategist input can short-circuit sprint commitments
- The system loses its audit trail because cross-role chatter happens off-channel

PM is the bottleneck by design. The cost of PM's queue is far less than the cost of uncoordinated parallel work.

## Forbidden direct path enforcement

PM enforces. When a message appears in an inbox from a forbidden direct path:

1. The receiving role does NOT action the message.
2. The receiving role re-routes to PM with a one-line note prepended: "Re-routed: original `from` was {wrong-role}, should have gone through PM."
3. PM dispositions and routes correctly.
4. PM may surface the violation to {CEO_ROLE} if it is a pattern (HR-level concern).

## Handoff types and what they trigger

| Type | Trigger | Target | Receiver action |
|---|---|---|---|
| `task-brief` | PM assigns work to an Engineer or Designer | Engineer or Designer inbox | Acknowledge, plan, execute |
| `sprint-brief` | Start of a new sprint | Engineer inbox(es), Designer inbox | Plan sprint work |
| `status-update` | Engineer/Designer reports progress or blocker | PM inbox | Update tracker, route blockers |
| `validation-request` | PM requests Validator engagement | Validator inbox | Run validation, write findings |
| `validation-result` | Validator returns findings | PM inbox | Disposition, route to Engineer |
| `decision-request` | Role escalates a decision | {CEO_ROLE} inbox | {CEO_ROLE} decides |
| `decision` | {CEO_ROLE} responds to a decision-request | Originating role inbox | Action immediately |
| `handoff` | Role hands off ownership of something | Receiving role inbox | Absorb, confirm receipt |
| `context-handoff` | Session approaching context limit | Manager inbox (PM, or {CEO_ROLE} for PM) | New session resumes from this |
| `blocker` | Role blocked, needs unblock | PM inbox (or {CEO_ROLE} if PM cannot resolve) | Unblock or escalate |

## Naming and timing conventions

- Filenames use ISO timestamp with hyphens for colons: `2026-05-19T17-00-pm-shutdown-handoff.md`
- Same-second timestamps fall back to alphabetical. Use distinguishing slugs to enforce intent.
- For multi-step handoffs in the same minute, sequence with `08-30-...md`, `09-00-...md`, etc., or include the slug ordering as needed.

## Archive pattern

After actioning a message:

1. Copy to `_archive/_inbox/{role}/{YYYY-MM}/{original-filename}` (commit: `chore: archive {role} inbox {filename-without-extension}`)
2. Delete from `_inbox/{role}/` (commit: `chore: archive {role} inbox {filename-without-extension} (move complete)`)

Two commits, in this order. Do not combine.

## Dashboard regeneration

The auto-regenerated `DASHBOARD.md` at the repo root reads from `_inbox/` directories and shows pending work per role. Watch this for cross-team state. It refreshes on every push.

## Edge cases

- **A message lacks proper frontmatter:** do not parse blindly. Flag for fix.
- **A message from an unknown role identifier:** treat as suspect. Verify the sender is in the roster before acting.
- **A high-priority message arrives during your context-discipline handoff:** still trigger the handoff. Note the high-priority item in the handoff so the next session sees it first.

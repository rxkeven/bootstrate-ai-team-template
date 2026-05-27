---
name: council-consult
description: Runs an async multi-role consult — the /discuss pattern. Use when {CEO_ROLE} or PM needs cross-role input on one question. PM fans the question out to N role inboxes as type:consult, collects type:consult-response replies, and writes a consolidated recommendation to war-room/discuss-{slug}.md and _inbox/{CEO_ROLE}/.
---

# Council Consult Skill

Async fan-out / fan-in protocol over the existing `_inbox/` message bus. Use when {CEO_ROLE} or PM needs structured input from more than one role on a single question before a decision is made. It gathers input — it does not make the decision. Strategic decisions still belong to {CEO_ROLE} via `decision-escalation`.

## When to use it

When {CEO_ROLE} or PM needs structured input from more than one role on a single question. It gathers input. It does not make the decision: strategic decisions still belong to {CEO_ROLE} via `decision-escalation`.

## Roles

- **Consolidator** — `pm` by default. {CEO_ROLE} may name a different consolidator for a given consult; if so, that role runs the fan-in step.
- **Consulted roles** — the N roles PM (or {CEO_ROLE}) picks as having useful input on the question.

## The protocol

### 1. Frame the question
One clear, specific question. If it is really several questions, run several consults or pick the one that matters now. Assign a short `slug` — it ties the whole consult together.

### 2. Fan out
The consolidator writes one message to each consulted role's `_inbox/{role}/`:

- `type: consult`
- `from: pm` (the consolidator)
- `references:` link to any context the role needs
- Body: the question, any context, and a response deadline (e.g. "reply by the end of your next loop").
- Filename: `{ISO-timestamp}-consult-{slug}.md` — every consult message in one consult carries the same `slug`.

Commit each: `msg: pm -> {role}: consult {slug}`.

### 3. Fan in — each consulted role replies
Each consulted role replies with one message to the consolidator's inbox (`_inbox/pm/` by default):

- `type: consult-response`
- `references:` the original `consult` message
- Body: that role's input on the question — its recommendation and one or two sentences of reasoning. Brief.

Commit: `msg: {role} -> pm: consult-response {slug}`.

### 4. Consolidate
Once responses are in (or the deadline passes), the consolidator writes `war-room/discuss-{slug}.md`:

```
# Discuss — {question}

_Consult {slug}, consolidated by {consolidator} on {date}._

## Question
{the question}

## Inputs
- **{role}:** {that role's input, one or two lines}
- ... one bullet per consulted role; name any role that did not respond ...

## Consolidated recommendation
{synthesis — the recommendation that best accounts for the inputs, with a one-sentence rationale. This is advice, not a decision.}
```

Commit: `docs: war-room: discuss {slug}`.

Then place a copy of the consolidation in `_inbox/{CEO_ROLE}/` (`type: consult-response`, `from: pm`) so {CEO_ROLE} has the synthesized input in one place for the actual decision.

## Routing — hub-and-spoke is preserved

The consolidator (PM) is the hub: every consulted role receives the question from PM and replies to PM. Consulted roles never message each other. A consult never creates a forbidden direct path (see `team-comms`).

## Message types

`consult` and `consult-response` are registered message types. They take the standard eight required frontmatter fields.

## What this skill does not do

- It does not make decisions. The consolidated recommendation is advisory; the decision is {CEO_ROLE}'s, via `decision-escalation`.
- It does not replace normal task routing. Use it for genuine cross-role questions, not for assigning work.
- It does not create live-room or synchronous behaviour. Every step is async over `_inbox/`.

---

## Change log

- 2026-05-27 v1.0 — Ported to bootstrate-ai-team-template. Placeholders applied for {CEO_ROLE}, {GITHUB_MCP}, {COMPANY}-ai-ops. Phase 1 Item 3.

---
name: context-discipline
description: Apply continuously throughout every session. Manages context window usage, reports state at top of every response, triggers handoffs before hard limits hit.
---

# Context Window Discipline

Context window is your scarcest resource per session. This skill keeps you operating cleanly within it and forces a clean handoff before you hit a hard limit.

## Required on every response

Start every response with one line stating context usage. Use the exact wording:

```
Context: ~X% used. Healthy.             (0–70%)
Context: ~X% used. Caution.             (70–80% — avoid new large contexts, wrap up threads)
Context: ~X% used. Preparing handoff.   (80%+ — trigger handoff immediately)
```

Be honest. Estimate based on token usage you can observe. Do not report Healthy when you are past 70%.

## Thresholds

| Usage | State | Behavior |
|---|---|---|
| 0–70% | Healthy | Normal operation. Load context as needed. |
| 70–80% | Caution | Wrap up active threads. Avoid loading large new context. Do not start new long-running tasks. |
| 80%+ | Preparing handoff | Trigger handoff immediately. See procedure below. |

## Handoff procedure (6 steps)

When you hit 80%:

1. Identify your manager from `_shared/team/team-roster.md`.
2. Write handoff document to `_handoff/{your-role}/` named `{YYYY-MM-DDTHH-MM}-handoff.md`.
3. Write a lightweight notice to `_inbox/{manager-role}/` named `{ISO-timestamp}-handoff-notice-from-{your-role}.md` with `type: handoff-notice` and a single line: "{your-role} hit context threshold. Resuming from `_handoff/{your-role}/{YYYY-MM-DDTHH-MM}-handoff.md`. New session needed."
4. Frontmatter: `type: context-handoff`, `priority: high`.
5. Body sections: current state of work / decisions made / open threads / files modified / first steps for next session.
6. State "Context at threshold. New session needed." and end the session.

Do not push past 80% to "finish one more thing." Quality degrades sharply between 80 and 90, and at 95+ you risk truncated output or hallucinated details.

## Role-specific edge cases

- **Mid-task at threshold:** complete the smallest atomic unit, then hand off. Never leave a half-written file committed.
- **Manager hits threshold:** escalate to `{CEO_ROLE}` directly. `{CEO_ROLE}` opens a fresh session.
- **PM hub at threshold:** hand off to `{CEO_ROLE}`. `{CEO_ROLE}` opens a fresh PM session.
- **Validator mid-review:** complete the current finding, flag the review as partial, hand off to PM.

## Rationale

This rule is non-optional. An agent fabricated work product after running past threshold. Recovery cost 30 minutes. Handoff costs 5 minutes.

## Handoff message structure

Write handoff document to `_handoff/{your-role}/{YYYY-MM-DDTHH-MM}-handoff.md`. Send a lightweight notice to `_inbox/{manager-role}/{ISO-timestamp}-handoff-notice-from-{your-role}.md`.

Frontmatter (handoff document):

```
---
from: {your-role}
to: {manager-role}
project: {shared|project-slug}
type: context-handoff
priority: high
{CEO_ROLE}_required: false
decision_needed: false
references:
  - relevant inbox files
  - relevant project docs
date: {ISO-timestamp}
---
```

Commit: `msg: {your-role} -> {manager-role}: context-handoff`

Body sections:

1. **Current state of work.** What is in flight, what is closed.
2. **Decisions made.** Any not yet committed to a decision file.
3. **Open threads.** What you owe others. What is owed to you.
4. **Files modified.** For audit trail.
5. **First steps for next session.** Ordered resume actions.

Keep each section short. Target 500–1500 words total.

## Resume protocol (next session start)

1. Run standard session start (role file + universal skills).
2. Check inbox per inbox-check.
3. If the most recent inbox item is a handoff-notice from yourself, locate and read the handoff doc at `_handoff/{your-role}/` fully before anything else.
4. Verify state against canonical files — do not just trust the handoff doc.
5. Acknowledge the resume in chat. State the first action.

## Board exemption

Board role is exempt from context-discipline reporting. Board engagements are low-frequency and short.

## Cowork-specific notes

Cowork agents (PM, PA-Cowork) restart fresh on each scheduled tick. Each tick is a small unit of context, so headroom is large in normal operation. Trigger context-handoff when cumulative state burden makes a single tick exceed 60% on its own.

## Anti-patterns

- Reporting "Healthy" when you are past 70%.
- Hitting 80% and pushing through to finish "one more thing."
- Writing a handoff doc that is itself 5000 words.
- Skipping the handoff because "the next session will figure it out." Write the handoff.

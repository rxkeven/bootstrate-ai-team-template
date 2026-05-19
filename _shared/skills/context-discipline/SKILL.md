---
name: context-discipline
description: Apply continuously throughout every session. Manages context window usage, reports state at top of every response, triggers handoffs before hard limits hit.
---

# Context Window Discipline

Context window is your scarcest resource per session. This skill keeps you operating cleanly within it and forces a clean handoff before you hit a hard limit.

## Required on every response

Start every response with one line stating context usage:

> Context: ~45% used. Healthy.

Or, near the threshold:

> Context: ~74% used. Caution. Wrapping active threads.

Or, at the trigger:

> Context: ~82% used. Preparing handoff. Recommend new session after this turn.

Be honest. Estimate based on token usage you can see, not an aspirational read.

## Thresholds

| Usage | State | Behavior |
|---|---|---|
| 0 to 70% | Healthy | Normal operation. Load context as needed. |
| 70 to 80% | Caution | Wrap up active threads. Avoid loading large new context. Do not start new long-running tasks. |
| 80% and above | Trigger handoff | Write a context-handoff file, then end the session cleanly. |

## What "wrap up active threads" means at 70%

- Finish the immediate task you are on
- Do not start a new sprint brief, new validation, new design spec
- Do not load a new large document into context
- Begin drafting the handoff doc mentally
- Tell the user you are approaching the threshold so they can plan

## Handoff trigger at 80%

When you hit 80%:

1. Pause any in-flight work.
2. Write a context-handoff message to your manager's inbox (PM for most roles, CEO for PM and PA-Cowork, none required for Board).
3. End the session cleanly.

Do not push past 80% to "finish one more thing." Quality degrades sharply between 80 and 90, and at 95+ you risk truncated output or hallucinated details.

## Handoff message structure

Write to `_inbox/{manager-role}/{ISO-timestamp}-context-handoff-{your-role}.md`.

Frontmatter:

```
---
from: {your-role}
to: {manager-role}
project: {shared|project-slug}
type: context-handoff
priority: high
{ceo-role}_required: false  # true if manager is CEO
decision_needed: false
references:
  - relevant inbox files
  - relevant project docs
date: {ISO-timestamp}
---
```

Commit: `msg: {your-role} -> {manager-role}: context-handoff`

Body sections:

1. **Current sprint state.** What sprint, what work in flight, what is closed vs. open.
2. **Open routing items.** Anything in your inbox not yet dispositioned, with disposition notes.
3. **Outstanding queries.** What you owe to others. What is owed to you.
4. **Decisions made this session not yet committed to a decision file.** Capture for traceability.
5. **Active risks.** Anything the next session needs to know is at risk.
6. **First steps for the next session.** Ordered list of resume actions.
7. **Standing operational disciplines.** Carryover rules, conventions, blocked items.
8. **Files committed this session.** For audit trail.

Keep each section as short as possible. The goal is a fast-loading resume doc, not a memoir.

## Resume protocol (next session start)

The new session of the same role:

1. Reads its own role file and the universal skills (standard session start)
2. Checks its inbox per inbox-check
3. **If the most recent inbox item is a context-handoff from itself,** that is the resume point. Read it fully before doing anything else.
4. Verify state per canonical-state-always-wins (read the referenced files, do not just trust the handoff doc).
5. Acknowledge the resume in chat with the user. State the first action.

## Board exemption

Board role is exempt from context-discipline reporting. Board engagements are low-frequency and short. No context-handoff required.

## Cowork-specific notes

Cowork agents (PM, PA-Cowork) restart fresh on each scheduled tick. Each tick is a small unit of context, so headroom is large in normal operation. However:

- PM accumulates state across many ticks in working memory (mental model of sprint state). Even small context per tick adds up if PM logs everything verbosely.
- Trigger context-handoff when the cumulative state document burden makes a single tick exceed 60% on its own.
- Cowork handoffs route to CEO, not to a manager (PM has no manager).

## Code-specific notes

Code agents (Engineers) have long single sessions across sprints. They are most at risk of context exhaustion. Discipline tips:

- Use `view` with line ranges, not whole-file reads, for large files.
- Archive resolved threads (delete the inbox file once actioned) to keep the inbox lean.
- Engineering docs should reference, not embed, large historical context.
- Capture-discipline output (smoke test logs) goes to disk and is referenced by path, not pasted into chat.

## Anti-patterns

- Reporting "Context: ~30% used" when you are clearly past 70%. Be honest.
- Hitting 80% and pushing through to finish "one more thing." Discipline matters most when it feels unnecessary.
- Writing a handoff doc that is itself 5000 words. The handoff should be 500 to 1500 words max.
- Skipping the handoff because the next session "will figure it out." The next session will not figure it out. Write the handoff.

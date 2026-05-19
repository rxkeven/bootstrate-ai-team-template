---
name: decision-escalation
description: Use when you encounter a decision outside your role's authority. Defines escalation criteria, message format, and what to do while waiting for a response.
---

# Decision Escalation Protocol

## When to escalate

Escalate to CEO via `_inbox/{ceo-role}/` when any of the following applies:

1. **Strategic forks.** Architecture decisions, scope changes that alter the roadmap, pivots in approach.
2. **Financial decisions.** Pricing, partnerships, hiring, capital, vendor commitments above your role's authority threshold.
3. **Legal or regulatory matters.** Contracts, compliance interpretation, partner agreements, terms of service.
4. **Inter-role conflicts you cannot resolve.** Two agents requesting opposite things and the resolution requires authority you do not have.
5. **Brand or voice changes.** Anything that would alter `_shared/brand/` standards or the consumer-facing identity.
6. **Sprint goals or roadmap priorities.** PM owns sprint execution; CEO owns sprint goals.
7. **Client relationships above the Client Care line.** CCS drafts; CEO approves and sends.
8. **Roster changes.** Adding, removing, or changing role surfaces. Routes through the HR skill but requires CEO authorization.
9. **OpSec ambiguity.** When operational security rules do not clearly cover the situation.
10. **Timeline risk past your sprint window.** Anything that pushes a milestone outside the agreed window.

When in doubt, escalate. The cost of a low-priority escalation is a few minutes of CEO attention. The cost of an unauthorized strategic move is much higher.

## When NOT to escalate

- Routine execution within your role's documented scope
- Implementation choices within an approved sprint brief
- Internal coordination handled by PM
- Tactical questions answered by reading the canonical docs (`vtlhlth-strategy.md`-equivalent, project north-stars, role files)
- Style or formatting questions covered by CLAUDE.md or brand docs

## How to escalate

Write a file to `_inbox/{ceo-role}/` per the team-comms protocol.

Frontmatter:

```
---
from: {your-role}
to: {ceo-role}
project: {shared|project-slug}
type: decision-request
priority: high  # urgent only if time-bound within 24h
{ceo-role}_required: true
decision_needed: true
references:
  - path/to/context-doc
date: 2026-05-19T14:30:00Z
---
```

Commit: `escalation: {your-role} -> {ceo-role}: {topic}`

## Body structure

Use this template:

```markdown
# {Short, specific title}

## Context

One paragraph. What is the situation, what is the relevant background.

## The decision

What specifically needs CEO authorization. State it clearly.

## Options

Present 2 to 3 meaningfully different approaches. Not minor variations. For each:

- One-line summary
- Pros (1 to 3 bullets)
- Cons (1 to 3 bullets)

## Recommendation

State your recommendation in one sentence. Reasoning in two sentences.

## What I will do if no response by {date}

State your default action so CEO is not the rate-limiter. If a default is dangerous (e.g., "I will proceed with the riskier option"), say "I will hold and re-surface."

## References

Link to canonical docs the decision relates to.
```

## After escalating

1. **Notify your immediate manager** (usually PM) that you have escalated and are blocked.
2. **Do not loop.** One escalation per decision. Do not write a second escalation in the same session unless the first is older than the priority window.
3. **Continue parallel work** that does not depend on the escalation outcome.
4. **Do not assume a verbal "go" replaces a written decision.** Per the inbox-check skill, verbal directives are pointers; the canonical record is the decision file CEO writes back to your inbox.

## When the CEO decision arrives

CEO writes back to your inbox with a `type: decision` message. The body documents the chosen option and any constraints. Action it immediately. Archive both the escalation and the decision file (two-commit pattern each).

If the decision is unclear or contradicts canonical state, surface the conflict before acting.

## Tone

- Brief. No padding.
- Recommendation first, reasoning second.
- Active voice.
- No hedging ("I think maybe possibly..."). State the recommendation clearly even if uncertainty is high; the CEO needs your best read, not a refusal to commit.

---
name: task-router
description: Deterministic request-type to owning-role decision tree for triaging inbound items in _inbox/{CEO_ROLE}/ and _inbox/pm/. Produces an advisory suggested-owner tag only; PM still confirms and routes. Unclassifiable items fall through to pm by design.
---

# Task Router Skill

Deterministic decision tree for triaging inbound requests. Derived from `owns`/`does-not-own` fields in `_shared/team/team-roster.md` and role definition files. If those change, update this tree to match.

## What this skill is — and is not

- Produces an **advisory tag only.** Does not assign work, does not move a message, does not change routing.
- **PM still confirms.** A `suggested-owner` tag is a hint; PM or {CEO_ROLE} reviews and makes the real call.
- **Hub-and-spoke is unchanged.**

## When to run it

On triage of a new inbound item in `_inbox/{CEO_ROLE}/` or `_inbox/pm/`. Run once per item when first read.

## How to apply

1. Read the request. Identify what is actually being asked for.
2. Walk the decision tree **top to bottom, first match wins.**
3. Record the result as a `suggested-owner:` line in the item's frontmatter.
4. Hand to PM as normal.

Never leave an item untagged. If you cannot classify with confidence, use the fail-safe.

## The decision tree (first match wins)

**A. Team itself** — roster, role definitions, boot prompts, onboarding, offboarding, team-health, self-improvement. → **`hr-manager`**
(Exception: if {CEO_ROLE} must *decide* the change, tag **`{CEO_ROLE}`**.)

**B. CEO-authority matters** — financials, legal, partner contracts, pricing, capital, hiring. → **`{CEO_ROLE}`**

**C. Board governance** — pressure-testing a major decision. → **`board`**

**D. Strategy** — architecture / scope / model rules, sprint-roadmap boundaries, strategy doc. → **`strategist`**

**E. Engineering / implementation.** Identify the project:
- Active project engineering work → **`engineer`** (append project slug for multi-engineer setups, e.g. `engineer-platform`)
- Project unclear or spans multiple → **`pm`** (PM decomposes)

**F. Code review / validation** — code review, architecture review, API contract check, test-coverage gap, claim-vs-implementation. → **`validator`**

**G. Design** — brand-to-product, spec docs, layout, states, responsive, accessibility. → **`designer`**

**H. Client communication** — drafting client-facing or client-care messages in {CEO_ROLE}'s voice. → **`ccs`**

**I. Portfolio / cross-project reporting** — performance reports, dependency radar, launch-readiness, stakeholder briefing, project intake. → **`portfolio-manager`**

**J. {CEO_ROLE}-inbox monitoring / relay** — watching `_inbox/{CEO_ROLE}/`, pushing notifications, relaying replies. → **`pa-cowork`**

**K. Project execution and coordination** — sprint briefs, task routing, milestone tracking, risk surfacing, cross-role items. → **`pm`**

## The fail-safe (mandatory)

If **any** of the following is true after walking A through K, tag the item **`pm`**:

- The request does not classify cleanly into one branch
- The request spans two or more owners
- The request is novel and no branch clearly fits
- You are not confident in the classification

`pm` is the catch-all owner by design. Fail safe, not fail open.

## Pointers

- Role definitions: `_shared/team/roles/`
- Roster: `_shared/team/team-roster.md`
- Routing topology: `_shared/team/handoff-protocols.md`

---

## Change log

- 2026-05-27 v1.0 — Ported to bootstrate-ai-team-template. Placeholders applied for {CEO_ROLE}, {GITHUB_MCP}, {COMPANY}. Phase 1 Item 5.

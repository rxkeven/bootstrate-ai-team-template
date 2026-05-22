---
name: hr
description: Use when adding a new team member to the AI roster, offboarding an existing one, or evaluating role gaps. Entry point for all roster changes.
---

# HR Skill

This skill is the entry point for any change to the AI team roster.

## When to trigger

- Adding a new role (additional engineer, dedicated researcher, second designer, etc.)
- Promoting a Chat-based role to Cowork or Code surface
- Offboarding an existing role permanently (not a session shutdown)
- Replacing the surface of an active role (e.g., moving CCS to a dedicated agent platform)
- Auditing the roster for gaps or overlap

Do NOT trigger for: routine session shutdown handoffs, normal context-discipline handoffs, or temporary role pauses. Those use existing handoff protocols.

## Roles

CEO and PM jointly own HR work. CEO authorizes; PM executes the runbooks. Strategist may surface gaps but does not own HR execution.

## Entry checklist

Before running the onboarding runbook, confirm:

1. **Authorization.** Has CEO approved this roster change? If not, escalate via `decision-escalation` first.
2. **Surface decision.** What surface is the role on (Chat, Cowork, Code, Console Managed Agent, custom)? Surface choice constrains tools available and onboarding steps.
3. **Inbox path.** Will the role need an inbox at `_inbox/{role}/`? If yes, the runbook creates it.
4. **Boot prompt.** Does a role prompt at `_shared/team/role-prompts/{role}.md` need to be drafted? Required for activation.
5. **Role definition.** Does a role definition at `_shared/team/roles/{role}.md` need to be drafted? Required for canonical identity.
6. **Roster update.** Will `_shared/team/team-roster.md` need a new row? Yes, in every onboarding.

If any answer is unclear, surface to CEO before starting the runbook.

## Full procedures

- **Onboarding:** `_shared/skills/hr/ONBOARDING.md` — 7-step workflow from role identification through activation.
- **Offboarding:** `_shared/skills/hr/OFFBOARDING.md` — 5-step workflow for permanent role retirement.

## Templates and patterns

- New Cowork role: model on existing `_shared/team/role-prompts/pm.md` or `pa-cowork.md`.
- New Code role: model on existing `_shared/team/role-prompts/engineer.md`.
- New Chat role: model on existing `_shared/team/role-prompts/strategist.md` or `designer.md`.
- New role definition: model on any file under `_shared/team/roles/`.

## Surface migration

When moving an existing role to a different surface (e.g., Chat to Cowork):

1. The role writes a context-handoff before shutdown.
2. New role file plus boot prompt for the new surface.
3. Old surface session ends; new surface session activates with the new boot prompt.
4. Roster update reflects new surface.

## Roster audit

Quarterly or when scope changes:

1. Read `_shared/team/team-roster.md`.
2. For each role, check active status and recent activity (inbox messages in the last 30 days).
3. Identify gaps (unmet recurring need) and overlaps (two roles owning the same thing).
4. Surface findings to CEO with recommendations.

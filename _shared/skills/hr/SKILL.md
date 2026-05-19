---
name: hr
description: Use when adding a new team member to the AI roster, offboarding an existing one, or evaluating role gaps. Wraps the full 10-step onboarding runbook with the entry-point checklist and triggers.
---

# HR Skill

This skill is the entry point for any change to the AI team roster. It is a thin wrapper around the existing 10-step runbook at `_shared/team/onboarding-new-team-member.md`. The runbook is canonical for procedures; this skill is canonical for when to invoke them.

## When to trigger

- Adding a new role (additional engineer, dedicated researcher, second designer, etc.)
- Promoting a Chat-based role to Cowork or Code surface
- Offboarding an existing role permanently (not a session shutdown)
- Replacing the surface of an active role (e.g., moving CCS to a dedicated agent platform)
- Auditing the roster for gaps or overlap

Do NOT trigger for: routine session shutdown handoffs, normal context-discipline handoffs, or temporary role pauses. Those use existing handoff protocols.

## Roles

CEO and PM jointly own HR work. CEO authorizes; PM executes the runbook. Strategist may surface gaps but does not own HR execution.

## Entry checklist

Before running the full onboarding runbook, confirm:

1. **Authorization.** Has CEO approved this roster change? If not, escalate via `decision-escalation` first.
2. **Surface decision.** What surface is the role on (Chat, Cowork, Code, Console Managed Agent, custom)? Surface choice constrains tools available and onboarding steps.
3. **Inbox path.** Will the role need an inbox at `_inbox/{role}/`? If yes, the runbook creates it.
4. **Boot prompt.** Does a role prompt at `_shared/team/role-prompts/{role}.md` need to be drafted? Required for activation.
5. **Role definition.** Does a role definition at `_shared/team/roles/{role}.md` need to be drafted? Required for canonical identity.
6. **Roster update.** Will `_shared/team/team-roster.md` need a new row? Yes, in every onboarding.

If any answer is unclear, surface to CEO before starting the runbook.

## Full procedure

Run the 10-step runbook at `_shared/team/onboarding-new-team-member.md`. The runbook covers: role spec drafting, brand and skill loading, inbox creation, scheduled-task setup (for Cowork), tool loading, first-cycle verification, roster commit, and activation announcement.

## Templates and patterns

- New Cowork role: model on existing `_shared/team/role-prompts/pm.md` or `pa-cowork.md`.
- New Code role: model on existing `_shared/team/role-prompts/engineer.md`.
- New Chat role: model on existing `_shared/team/role-prompts/strategist.md` or `designer.md`.
- New role definition: model on any file under `_shared/team/roles/`.

## Offboarding

When permanently retiring a role:

1. The role writes a final shutdown handoff to its manager's inbox.
2. PM archives all active inbox items for the role to `_archive/_inbox/{role}/`.
3. Update `_shared/team/team-roster.md` to mark the role retired with a date.
4. Keep the role files (`_shared/team/roles/{role}.md` and `_shared/team/role-prompts/{role}.md`) for reference; do not delete.
5. If the role had a scheduled task (Cowork), unregister it.

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

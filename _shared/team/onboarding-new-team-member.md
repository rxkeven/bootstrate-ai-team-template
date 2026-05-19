# Onboarding a New Team Member

The 10-step runbook for adding a role to the {COMPANY} AI team. PM executes; {CEO_ROLE} authorizes. The HR skill at `_shared/skills/hr/SKILL.md` is the entry point and confirms authorization before this runbook starts.

## Step 1: Draft the role definition

Create `_shared/team/roles/{new-role}.md` modeled on an existing role file. Required sections:

- Identifier, surface, status, reports-to, scope
- Owns
- Does not own
- Communication paths and forbidden direct paths
- Standing conventions
- Pointers to relevant docs

Commit: `feat: add role definition for {new-role}`

## Step 2: Draft the boot prompt

Create `_shared/team/role-prompts/{new-role}.md` modeled on an existing boot prompt. Required sections:

- One-line identity, surface, manager declaration
- Context-discipline reminder
- Role definition pointer
- Universal skills list
- Where things live (inbox path, manager inbox, related project paths)
- Tools to load (one ToolSearch line)
- Scope summary (DOs and DO NOTs)
- House rules pointer to CLAUDE.md
- First actions on session start
- Read-these-on-first-cycle reference list

Commit: `feat: add boot prompt for {new-role}`

## Step 3: Update the team roster

Add a row to `_shared/team/team-roster.md` with the new role's identifier, surface, manager, status, and start date. Add an entry to the change log.

Commit: `docs: roster add {new-role}`

## Step 4: Create the inbox directory

Create `_inbox/{new-role}/.gitkeep`. The empty inbox is now a valid target for messages.

Commit: `chore: create inbox for {new-role}`

## Step 5: Update handoff protocols if needed

If the new role introduces new communication paths or forbidden direct paths, update `_shared/team/handoff-protocols.md` to reflect them.

Commit: `docs: handoff protocols updated for {new-role}` (skip if no change)

## Step 6: Update the MCP availability matrix

If the new role's surface needs MCPs not previously documented, update `_shared/team/mcp-availability.md`.

Commit: `docs: mcp matrix updated for {new-role}` (skip if no change)

## Step 7: For Cowork roles, register the scheduled task

In the user's Claude Cowork environment:

1. Open a session for the new role with the boot prompt
2. The boot prompt instructs registration via `mcp__scheduled-tasks__list_scheduled_tasks` plus `update_scheduled_task` (or create)
3. Verify the task is registered with the expected cron and task ID

Skip this step for non-Cowork roles.

## Step 8: First cycle verification

Run a verification cycle:

1. Send a test message to the new role's inbox from PM (or the appropriate manager)
2. Confirm the role's session reads the message correctly
3. Confirm the role responds per protocol (back to PM inbox)
4. Confirm the dashboard reflects the activity on next regen

If any step fails, debug before announcing activation.

## Step 9: Activation announcement

PM writes a `status-update` to `_inbox/{CEO_ROLE}/` confirming activation. Include:

- Role identifier
- Start date
- First-cycle verification status
- Any open items (e.g., pending MCP setup, pending integration to other tools)

Commit: `msg: pm -> {CEO_ROLE}: new role activated ({new-role})`

## Step 10: Update CLAUDE.md if needed

If the new role introduces new house rules, escalation paths, or structural changes, update `CLAUDE.md`. Most additions do not require this.

Commit: `docs: CLAUDE.md updated for {new-role}` (skip if no change)

## After all 10 steps

The role is now in the canonical roster, has a defined identity and operational prompt, has an inbox to receive messages, and has passed first-cycle verification.

## Offboarding

To retire a role:

1. Final shutdown handoff from the role to its manager
2. Archive all active inbox items to `_archive/_inbox/{role}/`
3. Mark the role retired in `_shared/team/team-roster.md` with date and reason
4. Keep the role files in place for reference; do not delete
5. Unregister scheduled tasks (Cowork) if applicable
6. Notify {CEO_ROLE} via status-update

## Surface migration (e.g., Chat to Cowork)

1. Role writes a context-handoff before shutdown of old surface
2. Update the boot prompt at `_shared/team/role-prompts/{role}.md` for the new surface
3. Update the role definition's `Surface:` line at `_shared/team/roles/{role}.md`
4. Update `_shared/team/team-roster.md` to reflect new surface
5. Start the new surface session with the new boot prompt

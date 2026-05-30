# Onboarding a New Team Member

7-step process. CEO or Strategist identifies the need; PM executes steps 2 through 6; CEO activates in step 7.

## Steps

### 1. Identify the need (CEO or Strategist)

CEO or Strategist identifies a gap in team coverage and notifies PM via `_inbox/pm/` with a `type: task-brief` describing the role needed, the surface, and the reason.

### 2. Create the role file (PM)

Create `_shared/team/roles/{role}.md`. Model on existing role files. Include: identifier, surface, status, reports-to, owns, does-not-own, communication boundaries, standing conventions, pointers.

### 3. Create the boot prompt (PM)

Create `_shared/team/role-prompts/{role}.md`. Model on the prompt for the same surface type:

- Cowork role: model on `pa-cowork.md` or `pm.md`
- Code role: model on `engineer.md`
- Chat role: model on `strategist.md` or `designer.md`

Boot prompt must include: identity statement, role definition pointer, universal skills list, where things live, first actions, and the boot-prompt identity anchor section.

### 4. Create the inbox (PM)

Create `_inbox/{role}/.gitkeep`.

Commit: `chore: create inbox for {role}`

### 5. Update the roster (PM)

Add the new role row to `_shared/team/team-roster.md`. Include: role name, identifier, surface, status, reports-to.

### 6. File the welcome brief (PM)

Create a `type: task-brief` in `_inbox/{role}/` introducing the role, linking to its role file and boot prompt, and stating first-session expectations.

Commit: `msg: pm -> {role}: welcome brief`

### 7. Activate (CEO)

CEO opens the appropriate surface and pastes the boot prompt from `_shared/team/role-prompts/{role}.md`. New session begins.

## Notes

- Steps 2 through 5 can be committed in a single push.
- If the new role needs a scheduled task (Cowork), include setup instructions in the welcome brief.
- Notify PM when step 7 is complete so PM can issue the first sprint brief.

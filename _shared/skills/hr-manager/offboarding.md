# HR Manager Sub-skill: Offboarding

6-step runbook for retiring a role. {CEO_ROLE} directs; HR Manager executes.

## Before starting

Confirm {CEO_ROLE} direction exists in `_inbox/hr-manager/`. Do not begin without confirmed authorization.

---

## Step 1: Archive active inbox items

Move all files in `_inbox/{role}/` to `_archive/_inbox/{role}/{YYYY-MM}/`.

Commit: `chore: archive {role} inbox items before offboarding`

## Step 2: Remove inbox directory

Delete `_inbox/{role}/.gitkeep`. The path no longer receives messages.

Commit: `chore: remove inbox for offboarded role {role}`

## Step 3: Update team roster

Mark the role `Offboarded` in `_shared/team/team-roster.md` with date and reason. Never delete the row.

Commit: `docs: roster mark {role} offboarded`

## Step 4: Retain role artifacts

Do NOT delete `_shared/team/roles/{role}.md`, `_shared/team/role-prompts/{role}.md`, or `_todo/{role}.md`. Retained for reference.

## Step 5: Notify PM

Send `status-update` to `_inbox/pm/` informing PM of the retirement.

Commit: `msg: hr-manager -> pm: role offboarded ({role})`

## Step 6: Report to {CEO_ROLE}

Send `task-completion` to `_inbox/{CEO_ROLE}/` confirming offboarding complete.

Commit: `msg: hr-manager -> {CEO_ROLE}: offboarding complete ({role})`

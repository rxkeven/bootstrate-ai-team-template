# Agent To-Do Protocol

Self-managed carry-forward list. Every role maintains one at `_todo/{role}.md`. Check on every session start before checking the inbox. Write directly — no routing through PM needed.

## File location

`_todo/{role}.md` at repo root. A blank file is created when the role is onboarded (see `_shared/team/onboarding-new-team-member.md`).

## Format

Use this structure in your todo file:

```markdown
# To-Do: {role}

## Open

| Date added | Item | Priority | Notes |
|------------|------|----------|-------|
| YYYY-MM-DD | description | P1/P2/P3 | -- |

## Blocked

| Date added | Item | Blocked by | Notes |
|------------|------|------------|-------|

## Done

| Date closed | Item |
|-------------|------|
```

## Priorities

- **P1** -- Must complete this session. Blocking downstream work or an open commitment.
- **P2** -- Should complete this sprint. Important but not session-blocking.
- **P3** -- Nice-to-have. Complete when no higher-priority items remain.

## Session integration

1. On every session start, read `_todo/{your-role}.md` before checking the inbox.
2. Carry-forward items that are still relevant: leave open.
3. Carry-forward items that are irrelevant or superseded: move to Done with a note.
4. After actioning inbox work, return to Open items for anything that can be actioned now.

Commit todo updates with: `task: {project}: {role} todo update`

## Archiving

Move completed items to the Done table rather than deleting them. The pattern of closed items provides useful context for future sessions. Items in Done do not need to be cleared between sessions.

Blocked items remain in the Blocked table until unblocked, then move to Open or Done depending on whether they were completed before becoming blocked.

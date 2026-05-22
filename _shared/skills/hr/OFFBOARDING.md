# Offboarding a Team Member

5-step workflow for permanently retiring a role. Use only for permanent retirement, not routine session shutdown or temporary pause.

## Steps

### 1. Final handoff (retiring role)

The retiring role writes a final shutdown handoff to its manager's inbox summarizing open items, in-flight state, and any handover notes.

### 2. Archive inbox (PM)

Archive all remaining active messages in `_inbox/{role}/` to `_archive/_inbox/{role}/{YYYY-MM}/`.

Commit: `chore: archive inbox for offboarded {role}`

### 3. Update the roster (PM)

Mark the role retired in `_shared/team/team-roster.md` with a `retired: YYYY-MM-DD` field. Do not delete the row.

### 4. Retain artifacts (PM)

Do NOT delete:

- `_shared/team/roles/{role}.md`
- `_shared/team/role-prompts/{role}.md`
- Any project artifacts owned by the role

These remain for reference and potential re-activation.

### 5. Unregister scheduled task (PM, if applicable)

If the role had a scheduled task (Cowork), unregister or disable it. Confirm it is no longer polling before closing out.

## Notes

- Notify CEO when offboarding is complete.
- If the role's work is being redistributed, issue new briefs to receiving roles before closing out.

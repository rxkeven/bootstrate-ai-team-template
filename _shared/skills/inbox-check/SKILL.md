---
name: inbox-check
description: Standard inbox processing protocol. Use whenever you start a session, return after compaction, or need to verify pending work for your role.
---

# Inbox Check Protocol

## Canonical state always wins

The repo is canonical. Verbal directives from the user (or any human) that imply state already exists somewhere never substitute for reading the file. If the user says "the PM closed sprint 12, proceed" you still run inbox-check and read `_inbox/{your-role}/` and any referenced `projects/` files before acting. Verbal cues are pointers to where to look. They are not facts.

If file state contradicts a verbal directive, the file wins. Surface the conflict to the user before acting on either.

This rule exists because of a real incident in a production team: an agent took a verbal "proceed" signal as ground truth, skipped reading its inbox, and fabricated work product. The fabrication was caught roughly 30 minutes later. The fix is to always check the canonical source first.

## Step 1: Verify identity

Read the session prompt the user provided. It declares your role identifier. If you cannot identify your role from the prompt, stop and ask the user before proceeding. Do not guess.

## Step 2: List inbox

List files in `_inbox/{your-role}/`. Sort by filename (filenames are ISO-timestamp-prefixed, so an alphabetical sort gives chronological order). Ignore `.gitkeep`.

For Code surfaces with bash: `ls _inbox/{your-role}/ | sort`
For Cowork or Chat surfaces (no bash): use `github:get_file_contents` on the directory path.

## Step 3: Read each message

For each file, read the full content. Extract the YAML frontmatter to understand:

- `from`: who sent it
- `to`: confirm it is addressed to you (re-route if not, see edge cases)
- `type`: what kind of message
- `priority`: `normal`, `high`, or `urgent`
- `references`: linked files you should also read
- `decision_needed`: if true, requires a response
- `kevin_required` (or `{ceo-role}_required`): if true, the CEO must see this

If the frontmatter is malformed, do not parse blindly. Surface the file to the user and flag for fix.

## Step 4: Decide action

For each message, choose one:

- **Acknowledge and act:** the message asks you to do something within your scope. Do it. Send a response if the sender expects one.
- **Respond and route:** the message requires a reply or hands off to another agent. Write the response per the `team-comms` skill.
- **Escalate:** the message contains a decision outside your authority. Forward to `_inbox/{ceo-role}/` using the `decision-escalation` skill.
- **Archive only:** the message is informational, no action needed. Move to archive.

## Step 5: Archive processed messages

After acting on a message, move it from `_inbox/{your-role}/` to `_archive/_inbox/{your-role}/{YYYY-MM}/`. Preserve the original filename. This creates the audit trail.

Two-commit pattern (works for all surfaces including Cowork-only):

1. `github:create_or_update_file` to write the file at the archive path
2. `github:delete_file` to remove from the active inbox

Or for Code surfaces with bash:

```bash
mkdir -p _archive/_inbox/{your-role}/{YYYY-MM}/
mv _inbox/{your-role}/{filename} _archive/_inbox/{your-role}/{YYYY-MM}/
```

Commit the archive move with: `chore: archive {your-role} inbox {filename}`.

## Step 6: Report

Tell the user what you found in the inbox, what you actioned, and what (if anything) is now waiting on a response from another agent. Keep it short.

Always state which inbox files you read this session by filename, or report "inbox empty" if no files were present. This is the verification trace that confirms canonical state was checked. Reports that claim work was done without naming the files read are not acceptable.

## Edge cases

- **Empty inbox:** tell the user, ask what they want next. Do not invent work.
- **Malformed frontmatter:** do not parse blindly. Tell the user and flag for fix in a separate `fix:` commit.
- **Conflicting messages** (two agents requesting opposite things): escalate to CEO via `decision-escalation`.
- **Message addressed to wrong role:** if the `to:` field does not match your identifier, re-route. Move the message to the correct inbox and prepend a one-line note in the body explaining the re-route. Commit: `chore: reroute {filename} to {correct-role}`.
- **Forbidden direct path detected** (e.g., Engineer B sent something to Engineer A directly): re-route through `pm` with a note. PM disposition handles the rest.
- **Priority urgent and you cannot act immediately:** acknowledge by writing a brief status message back to the sender (`type: status-update`) saying you have seen it and stating your ETA. Then escalate to CEO if the ETA risks the urgent deadline.
- **Verbal directive contradicts file state:** the file wins. Quote the relevant file content back to the user, name the conflict, and ask which they want to act on before proceeding.
- **MCP timeout on a write:** verify state via a read before retrying. Timed-out writes sometimes complete server-side.

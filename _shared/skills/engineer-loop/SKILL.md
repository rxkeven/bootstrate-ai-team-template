---
name: engineer-loop
description: Use on Claude Code Engineer sessions to stay alive between active work cycles. Defines the inbox-loop-inbox cadence that replaces session restarts. Triggered after completing work, after escalating a blocker, or when the inbox is empty and you would otherwise end the session.
---

# Engineer Loop Protocol

This skill defines how an Engineer Claude Code session stays alive between active work cycles instead of ending and waiting for manual restart. The mechanism is Claude Code's `/loop` feature; the discipline is in this skill.

## Why this exists

Engineers on Claude Code are continuous-session roles in the Bootstrate operating model. PM Cowork polls every 30 minutes via a scheduled task. Engineers need an equivalent steady-state cadence on a surface that does not natively schedule. The `/loop` feature gives the Engineer a way to wait, then come back and check the inbox, then either act or wait again. Without this protocol, Engineers either end their session (forcing CEO to re-spawn) or sit idle producing no signal that they are alive.

## Loop syntax

`/loop` runs a prompt (or slash command) on a recurring interval:

```
/loop [interval] <prompt-or-command>
```

- **Explicit interval:** `/loop 30m check my inbox` — repeats the prompt every 30 minutes.
- **Self-paced (recommended for engineers):** `/loop check my inbox` — no interval; Claude uses `ScheduleWakeup` to set the delay dynamically based on context.

**Always provide a prompt.** The prompt tells Claude what to do each cycle. For engineers, the standard prompt is a variation of:

> `check my inbox and action any messages per the inbox-check skill`

**Use self-paced mode by default.** Self-paced mode lets Claude adjust timing dynamically — shorter during active sprints, longer when idle — which is more appropriate than a fixed interval. The duration targets in this skill are intended as `ScheduleWakeup` delay guidelines for self-paced mode, not as `/loop` interval arguments.

## When the loop applies

Enter the loop after any of:

1. **Completing a task.** You finished the work in a brief; status sent to PM; nothing else in inbox right now.
2. **Surfacing a blocker.** You wrote a blocker to PM and have no parallel work to do while waiting.
3. **Inbox empty on session start.** You came back from a previous loop, checked inbox, nothing there, no work in flight.

Do NOT enter the loop:

1. **During active work.** Work proceeds normally; the loop is for between-work waiting only.
2. **At context budget 80%+.** Trigger context-handoff first per context-discipline skill. Do not loop past the threshold.
3. **When all your work depends on a pending CEO escalation AND you have no parallel work.** End the session cleanly; the CEO re-spawns when the decision is ready. Looping with literally nothing to do wastes the session.
4. **After 3 empty checks in a row.** Write a status-update to PM ("idle, 3 empty cycles, ending session") and end. CEO will re-spawn when work returns.

## The cycle

```
[work or inbox check]
        |
        v
[any items to action?]
        |
   yes  |  no
        v
   [action] -> [status to PM] -> [/loop]
                                    |
                                    v (ScheduleWakeup fires)
                              [check inbox]
                                    |
                                    +---> back to top
```

In words:

1. Run inbox-check per the `inbox-check` skill.
2. If there are items, action them per their disposition. If you write status back to PM, include "looping again on completion" so PM knows you are still alive.
3. If the inbox is empty after action, invoke `/loop` (self-paced) with the standard inbox-check prompt. Claude will call `ScheduleWakeup` with the appropriate delay from the duration table below.
4. When the loop terminates, immediately run inbox-check again.
5. If 3 loops complete with empty inbox each time, exit per the boundary rules below.

## Loop duration

These are target delays for `ScheduleWakeup` when running in self-paced mode. They are not `/loop` interval arguments.

Default: **30 minutes** (1800 seconds). This matches PM Cowork's polling cadence, so PM's next tick and your next inbox check stay roughly in sync.

Adjust:

- **Active sprint windows:** 15 minutes. Faster feedback when work is flowing.
- **Waiting on external dependency** (deploy, third-party response, slow build): 60 minutes. Stop pestering yourself.
- **Waiting on a CEO decision and you have parallel work:** 30 minutes. CEO decisions tend to arrive in 1 to 4 hours; faster cycles capture them sooner.

If you change the duration mid-session, log it in your next status-update to PM. PM uses your cadence to plan its own dispatches.

## Boundary rules

| Situation | Action |
|---|---|
| Inbox empty 3 loops in a row | Status-update to PM ("idle, ending session, re-spawn when work returns"); end |
| Context budget hits 80% | Context-handoff to PM per context-discipline; end |
| You blocked on CEO escalation with no parallel work | End session immediately; CEO re-spawns on decision |
| New work arrives mid-loop | Loop will not interrupt; finish loop, then inbox-check picks it up |
| You finished a sprint and PM has not issued the next brief | Loop with standard duration; PM may be on next tick |
| Loop produces an error mid-cycle | Surface to user as a `fix:` commit candidate; do not assume the loop is broken until verified |

## Reporting cadence

Every time you re-enter active work from an empty-loop wake, prepend a one-line "wake from loop N" note to your first status-update. Lets PM and CEO see the cadence is alive.

Example:

```markdown
[wake from loop 4 of session]

# Status: migration step 3 complete

Migrated user_session table. Smoke test green. Moving to step 4 (foreign keys).
```

## Why this is not just "scheduled tasks"

PM uses scheduled tasks on Cowork because Cowork has no `/loop` and Cowork tick context is small. Engineer uses `/loop` on Code because:

1. Code surfaces have long single-session context budgets; restarting loses state.
2. `/loop` keeps the session and its working memory alive.
3. Engineering work often produces partial state (open files, queued tests) that benefits from persistence.

If a role's work is mostly stateless coordination (PM, PA), use Cowork + scheduled tasks. If a role's work accumulates state across cycles (Engineer), use Code + `/loop`.

## Anti-patterns

- **Looping when blocked with no parallel work.** You are paying session lifetime for nothing. End cleanly.
- **Looping silently.** PM and CEO do not know whether you are alive. Always write a status-update before you loop, and a "wake from loop" line when you re-enter active work.
- **Looping past context threshold.** Quality degrades sharply past 80% even on a fresh task. Hand off first; the next session can loop fresh.
- **Looping forever.** The 3-empty-cycles boundary is the floor. If something is genuinely wrong (PM not responding, dashboard frozen), surface it and end.
- **Omitting the prompt from `/loop`.** Without a prompt, `/loop` has no instructions to repeat each cycle. Always include the inbox-check prompt or a slash command.

## First actions for a session using this skill

Engineer's first-cycle reads now include this skill alongside the four universal skills. On every Engineer session:

1. Read role file at `_shared/team/roles/engineer.md`
2. Read the four universal skills under `_shared/skills/`
3. Read this skill at `_shared/skills/engineer-loop/SKILL.md`
4. Check `_inbox/engineer/` per inbox-check
5. Action items, status, then enter the loop per this protocol

## Interaction with context-discipline

`context-discipline` always wins. If you are about to invoke `/loop` and your context is at 80%+, switch to handoff path. The next session starts fresh and resumes the loop after reading your handoff.

If your context is at 70-80% (Caution), invoke `/loop` with a shorter ScheduleWakeup target (15 min) and use the wake to wind down active threads. Plan for a context-handoff within the next 1-2 cycles rather than at the very last tick.

# Decision: /loop behavior verification

**Date:** 2026-05-21  
**Author:** bs-code-eng  
**Status:** Confirmed — skill corrected

## Context

The `engineer-loop/SKILL.md` described `/loop` as a command that takes a duration argument, e.g. "issue `/loop` with the standard duration." The handoff doc flagged this as unverified and marked it the single most important thing to check in the first bs-code-eng session, because engineers running Claude Code are the ones actually invoking `/loop`.

## Findings

**Actual `/loop` syntax:**

```
/loop [interval] <prompt-or-command>
```

1. **`/loop` requires a prompt argument.** The prompt tells Claude what to do each cycle. Invoking `/loop 30m` with no prompt gives Claude nothing to execute.

2. **Self-paced mode (no interval) is supported and recommended.** Omitting the interval activates self-paced mode: Claude runs the prompt once, then calls `ScheduleWakeup` to set its own delay before the next iteration. This is better than a fixed interval for engineers because timing can adapt to context (15 min during active sprints, 30 min standard, 60 min waiting on external dependency).

3. **Duration targets map to `ScheduleWakeup.delaySeconds`, not to `/loop` interval arguments.** The 15/30/60 minute guidance in the skill is correct as a target, but it is the value Claude passes to `ScheduleWakeup` in self-paced mode — not a `/loop` parameter.

## What was wrong in the skill

- "Issue `/loop` with the standard duration" implied typing `/loop 30m` with no prompt. This is incomplete usage.
- The duration table did not clarify whether durations were `/loop` arguments or `ScheduleWakeup` targets.
- No guidance on what prompt to provide.

## Changes made

Updated `_shared/skills/engineer-loop/SKILL.md`:

- Added **Loop syntax** section with explicit format and examples.
- Changed all "issue `/loop` with the standard duration" phrasing to "invoke `/loop` (self-paced) with the standard inbox-check prompt."
- Reframed the **Loop duration** section as ScheduleWakeup delay targets.
- Added anti-pattern: **Omitting the prompt from `/loop`**.
- Updated **Interaction with context-discipline** to match corrected terminology.

## No architectural change

The engineer-loop pattern itself is unchanged. The loop cadence, boundary rules, and reporting conventions are all valid. Only the `/loop` command description was inaccurate.

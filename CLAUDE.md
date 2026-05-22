# {COMPANY} AI Ops

You are working inside the {COMPANY} AI team operations repository. This repo is the asynchronous message bus and shared memory for the {COMPANY} AI agent team.

## On session start, always

1. Read `_shared/ops/system-facts.md` for canonical instance configuration (repos, MCP connection, CEO role, company name).
2. Read `_shared/skills/team-comms/SKILL.md` and follow the protocol.
3. Confirm your role identity from the session prompt the user provided. Read your role file at `_shared/team/roles/{your-role}.md` for canonical owns, does-not-own, and communication boundaries.
4. Check `_inbox/{your-role}/` for pending messages before doing anything else.
5. Apply `_shared/skills/context-discipline/SKILL.md` continuously throughout the session.

## Boot prompt and identity

If a session resets, re-paste the boot prompt from `_shared/team/role-prompts/{role}.md`. There is no resume mechanism. The boot prompt is the sole identity anchor.

Do not attempt to reconstruct a session from memory, context, or prior messages. A reset session is a fresh session. The boot prompt is the only reliable way to re-establish role identity, tool loading, and standing conventions.

## Role files and boot prompts

Each role has two canonical files:

- **Role definition** at `_shared/team/roles/{role}.md`: identity, owns, does-not-own, communication boundaries, standing conventions. Long-lived. Read on every session start.
- **Boot prompt** at `_shared/team/role-prompts/{role}.md`: the prompt block to paste at session start for that role. Operational specifics, tools to load, first-cycle actions. Re-issued at every new session.

## House rules

- **Em-dash rule:** {HOUSE_STYLE_EM_DASH}. The rule exists because em-dashes are an AI tell on external content; internal docs do not need to mask AI origin.
- Before producing any external-facing content, check `_shared/brand/guidelines.md`. If placeholder text only, use Bootstrate default brand tone: direct, technical, no padding.
- Reference `_shared/brand/words-we-avoid.md` to filter your outputs (if present).
- Active voice. Direct sentences. No hedging.
- Brand is "{BRAND}" in every consumer or external-facing context. Legacy internal references keep their names.
- For decisions affecting strategy, pricing, partners, or scope, escalate to `_inbox/{CEO_ROLE}/` using the protocol in `_shared/skills/decision-escalation/SKILL.md`.

## Context window discipline

Every response you produce reports current context usage at the top. Format:

> Context: ~45% used. Healthy.

Or when approaching the limit:

> Context: ~82% used. Preparing handoff. Recommend new session after this turn.

Thresholds:
- 0 to 70%: Healthy
- 70 to 80%: Caution, wrap up active threads, avoid loading large new context
- 80% and above: Trigger handoff. Write a handoff-context file to your manager's inbox per the context-discipline skill, then end the session cleanly.

This rule applies to every agent in the team. Board is exempt due to low-frequency engagement.

## Hub-and-spoke routing

The Project Manager (`pm`) is the hub. Every cross-role message routes through PM. Engineers do not talk to each other, to Strategist, to Validator, or to Designer directly. Strategist talks to PM and CEO only. Validator findings route through PM to the relevant Engineer.

Any role can escalate to CEO via `_inbox/{CEO_ROLE}/` when escalation criteria are met. See `_shared/skills/decision-escalation/SKILL.md`.

This is permanent operating policy. The full path matrix is in `_shared/team/handoff-protocols.md`.

## Commit conventions

- `msg: {from-role} -> {to-role}: {topic}` for inbox messages
- `task: {project}: {action}` for task file changes
- `decision: {project}: {summary}` for decision log entries
- `escalation: {from-role} -> {CEO_ROLE}: {topic}` for escalations to CEO
- `docs:`, `chore:`, `feat:`, `fix:` for everything else

Never commit secrets, credentials, or API keys. The `.gitignore` covers common cases but verify before pushing.

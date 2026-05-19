# AI Team Template (V1.0)

A reusable scaffold for spinning up an AI agent team on the hub-and-spoke model. Provides the universal skills, role definitions, boot prompts, and operational docs needed to run a coordinated team of Claude agents (Cowork, Code, Chat, Console Managed Agent surfaces) for a single company or project portfolio.

This pattern was validated in production at Vital Health (vitalhealth-ai-ops) before generalization.

## What this gives you

- **Hub-and-spoke coordination** through a Project Manager agent
- **Asynchronous message bus** via a private GitHub repo with `_inbox/{role}/` directories
- **Four universal skills** every agent runs on session start (team-comms, inbox-check, decision-escalation, context-discipline)
- **Per-role definitions** at `_shared/team/roles/{role}.md` for canonical identity
- **Per-role boot prompts** at `_shared/team/role-prompts/{role}.md` for fast session startup
- **HR skill** for adding or offboarding agents
- **Auto-regenerating dashboard** on every push showing pending items and active work
- **Bootstrap orchestrator skill** at `_shared/skills/ai-team-bootstrap/SKILL.md` that walks you through standing up a new team

## How to use

### Option 1: Bootstrap a new team (most common)

1. Create an empty private GitHub repo for your target company (e.g., `{your-org}/your-company-ai-ops`)
2. Open a fresh Claude chat with GitHub MCP configured
3. Paste the contents of `BOOTSTRAP.md` as the first message
4. Provide the target repo coordinates when asked
5. Walk through the six-step orchestrator (discovery, audit, build plan, scaffold, handoffs if any, onboarding package)
6. End state: a fully scaffolded ops repo ready for first activation

### Option 2: Manually populate a target repo

If you prefer to skip the wizard and just copy the scaffolds:

1. Clone this template repo
2. Copy the `_shared/`, `_inbox/`, `_archive/`, `projects/` directories plus `CLAUDE.md`, `DASHBOARD.md`, `scripts/`, and `.github/workflows/` to your target repo
3. Read `_shared/team/placeholders.md` for the canonical placeholder list. Substitute every orchestrator-managed entry (universal and per-project) by hand. After substitution, grep your repo for the pattern `{[A-Z_]+}` to confirm nothing was missed; the only legitimate remaining match is `{WILL_BE_REPLACED_BY_SCRIPT}` in `DASHBOARD.md`, which the dashboard script fills on first push.
4. Set the GitHub Actions repository variables `CEO_ROLE` and `COMPANY` on your target repo so the dashboard regen labels correctly.
5. Customize role files and boot prompts as needed for your team. Update `_shared/team/team-roster.md` with the active roles and start dates.
6. Run the first-flight runbook at `_shared/team/first-flight-runbook.md` to confirm the round-trip works before live use.

## Placeholder conventions

Template files use ~17 placeholders that get substituted during bootstrap. The canonical list, with type, description, source question, and example for each, lives at `_shared/team/placeholders.md`. Read that file before doing any manual scaffolding (Option 2).

Key high-level points:

- **Orchestrator-managed:** `{COMPANY}`, `{COMPANY_SLUG}`, `{BRAND}`, `{CEO_ROLE}`, `{TEMPLATE_OWNER}`, `{TARGET_OWNER}`, `{TARGET_REPO}`, `{HOUSE_STYLE_EM_DASH}`, `{DATE}` — set once at scaffold time.
- **Orchestrator-managed, per-project:** `{PROJECT}`, `{PROJECT_SLUG}`, `{PROJECT_OR_ALL}`, `{REPO_URL}`, `{TECH_STACK}`, `{TECH_STACK_SUMMARY}`, `{MIGRATION_TOOLING_IF_APPLICABLE}` — substituted per project file.
- **Script-managed:** `{WILL_BE_REPLACED_BY_SCRIPT}` — the dashboard script fills this on every push.
- **In-content variables (never substitute):** lowercase placeholders like `{your-role}`, `{ceo-role}`, `{manager-role}` describe runtime behavior and are interpreted by agents, not replaced at scaffold time. See the registry for the full list.

## Standard roster

The template provides eight standard role definitions. Use what fits, drop what does not.

| Role | Surface | Typical engagement |
|---|---|---|
| `pm` | Claude Cowork | Continuous, 30-minute polling cadence. The hub. |
| `engineer` | Claude Code | Continuous, per project. Multiple instances allowed (one per project). |
| `designer` | Claude Chat | On-demand, per design sprint. |
| `strategist` | Claude Chat | On-demand, for strategic forks. |
| `validator` | Console Managed Agent | Per-checkpoint, on-demand. |
| `ccs` | Claude Chat | Continuous, until handed off to a Hermes-style dedicated agent. |
| `board` | Claude Chat | Weekly. |
| `pa-cowork` | Claude Cowork | Continuous, 30-minute polling cadence. Monitors CEO inbox only. |

## What is not included in V1.0

- Industry-specific defaults (healthcare, fintech, e-commerce)
- Visual UI wizard
- Automated MCP configuration
- Dashboard customization beyond the auto-regen script
- Cross-template skill updates (no automatic propagation)
- Skill testing harness

These are V1.1+ considerations.

## Provenance

V1.0 derived from `vitality-health/vitalhealth-ai-ops` after the per-role-file plus boot-prompt restructure committed 2026-05-19. Design spec at `2026-05-19T18-25-ai-team-bootstrap-v1-design.md` in that repo.

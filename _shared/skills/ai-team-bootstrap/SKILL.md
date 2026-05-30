---
name: ai-team-bootstrap
description: Use during a bootstrap engagement to scaffold a new AI agent team for a company or project. Walks six sequential steps (discovery, audit, build plan, scaffold push, optional handoffs, onboarding package) and writes outputs to a target empty GitHub repo. Triggered by the BOOTSTRAP.md entry prompt.
---

# AI Team Bootstrap Orchestrator

This skill walks you through standing up a new AI agent team from scratch. Read it in full before starting. Execute the steps in order. Do not skip ahead.

## Pre-flight check

Before Step 1:

1. Confirm you have GitHub MCP access (test with a read on the template repo's `README.md`).
2. Get the target repo coordinates from the user: `{TARGET_OWNER}` and `{TARGET_REPO}`. The target repo must already exist (empty, private, default branch `main`). If not, ask the user to create it before proceeding.
3. Confirm the user understands the engagement scope: six steps, ~30 to 60 minutes of conversation, ending with a scaffolded ops repo ready for first activation.

## Step 1: Discovery (company plus project)

Goal: capture the context that shapes scaffold customization.

Ask the following questions, one or two per message, not all at once:

1. Company name and one-line description.
2. Industries served. Any regulatory exposure worth flagging (HIPAA, SOC 2, GDPR, financial services, etc.)?
3. Brand voice characteristics. Pick or describe: formal, casual, credible insider, technical, friendly, authoritative, etc.
4. House style rules to enforce. Em-dash rule (forbidden in external, allowed in internal)? Other punctuation preferences? Banned words?
5. How many projects? List each with a one-line description.
6. Tech stack per project (e.g., Next.js plus Supabase plus Tailwind).
7. Existing code repo URLs (or new repo names to create separately).
8. CEO or primary decision-maker name (this becomes the escalation target).
9. Consumer-facing brand name if different from company name.
10. Anything else Claude should know about how this company works.

After answers:

- Synthesize into a structured doc.
- Write to target repo at `_bootstrap/01-discovery.md` (commit message: `docs: bootstrap step 1 discovery captured`).
- Present a one-screen summary in chat for user confirmation before moving to Step 2.

## Step 2: Audit (existing AI plus humans plus tools)

Goal: understand what is already running, what migrates, what new pieces are needed.

Ask:

1. Existing AI usage. Any Claude sessions in flight, ChatGPT agents, other models running? What do they own?
2. Human team members. Names and roles. Who maps to which AI role (CEO, PM, Engineer, Designer, etc.)?
3. Automation tools in active use. n8n, Make, Zapier, Airtable, Notion, Linear, Jira, others?
4. MCPs already configured in the user's Claude Desktop. Which ones will the new team need (GitHub, Supabase, Vercel, n8n, Higgsfield, Airtable, etc.)?
5. Communication tools. Slack, iMessage, email, Discord. Which roles will need which?
6. Anything migrating from a prior setup that needs preserved state? Existing inbox content, decision logs, ongoing sprint work?
7. Existing GitHub org or account where the target repo lives.

After answers:

- Write to target repo at `_bootstrap/02-audit.md`.
- Note any MCP gaps that will block specific role activation. Surface to user before Step 3.

## Step 3: Build plan synthesis (with approval gate)

Goal: convert raw answers into a concrete roster plus customization plan. Present for explicit user approval before scaffolding.

Produce:

1. **Recommended role roster.** Default is the eight standard roles (pm, engineer, designer, strategist, validator, ccs, board, pa-cowork). Drop, duplicate, or add roles based on Step 1 plus 2 answers. Justify each decision in one sentence.
2. **Surface decisions.** Map each role to a Claude surface (Code, Cowork, Chat, Console Managed Agent, Hermes-style custom).
3. **Cadence decisions.** Cowork polling intervals. Default `*/30 * * * *` for PM and PA; adjust if user has specific needs.
4. **CLAUDE.md customization plan.** Company name, brand rules, em-dash policy, project list, escalation target.
5. **Project north-star priorities.** Which projects need a `projects/{project}/project-north-star.md`? Strategist owns these post-activation.
6. **MCP availability matrix.** From the audit, which roles get which MCPs. Note any gaps where a role needs a tool that is not yet configured.
7. **Multi-engineer handling.** If the company has multiple projects, decide whether to duplicate the `engineer` role (one per project, e.g., `engineer-platform`, `engineer-quiz`) or run a single engineer rotating projects. Recommend duplication for clean ownership boundaries.

**Gate:** Present the plan in chat. Wait for explicit user approval (or amendments) before moving to Step 4. Do not commit anything to the target repo at this step until approved. Once approved, commit the build plan to `_bootstrap/03-build-plan.md`.

## Step 4: Scaffold push

Goal: populate the target repo with all customized files. This is where the team comes to life as a set of files.

Procedure:

1. Read each template file from `{TEMPLATE_OWNER}/bootstrate-ai-team-template`. Files to pull (in order):
   - `CLAUDE.md` (top-level)
   - `DASHBOARD.md` (top-level)
   - `scripts/update_dashboard.py`
   - `.github/workflows/update-dashboard.yml`
   - `_shared/skills/team-comms/SKILL.md`
   - `_shared/skills/inbox-check/SKILL.md`
   - `_shared/skills/decision-escalation/SKILL.md`
   - `_shared/skills/context-discipline/SKILL.md`
   - `_shared/skills/hr/SKILL.md`
   - `_shared/skills/engineer-loop/SKILL.md`
   - `_shared/team/roles/{role}.md` for each role in the approved roster
   - `_shared/team/role-prompts/{role}.md` for each role in the approved roster
   - `_shared/team/team-roster.md`
   - `_shared/team/handoff-protocols.md`
   - `_shared/team/onboarding-new-team-member.md`
   - `_shared/team/mcp-availability.md`
   - `_shared/team/placeholders.md`
   - `_shared/team/first-flight-runbook.md`
   - `_shared/brand/voice-guidelines.md` (stub; user customizes after bootstrap)
   - `_shared/brand/words-we-avoid.md` (stub; user customizes after bootstrap)
2. For each file, apply placeholder substitutions by iterating the canonical registry at `_shared/team/placeholders.md`. Pull the full registry once before substitution starts; do not hardcode a subset. The two orchestrator-managed tables (one universal, one per-project) cover every value that needs substitution. The script-managed placeholder (`{WILL_BE_REPLACED_BY_SCRIPT}`) and the in-content variables (lowercase, e.g., `{your-role}`) must be left untouched.

   For project-scoped files (engineer role, engineer boot prompt, validator role), run the per-project substitution loop once per project in the approved roster, producing one output file per project per source file.

   After substitution but before commit, grep each `.md` and `.yml` file for any remaining `{[A-Z_]+}` pattern. If any uppercase placeholder remains, halt and surface to the user. Do not commit files with unfilled placeholders.

   Exception: `DASHBOARD.md` legitimately contains `{WILL_BE_REPLACED_BY_SCRIPT}`, which is replaced on first push by the dashboard regen GitHub Action. Do not flag this one. Do not include `.py` files in the residue check; `scripts/update_dashboard.py` contains literal `{COMPANY}` and `{CEO_ROLE}` strings that are Python f-string variables read from environment, not template placeholders.
3. Batch the pushes into logical commits:
   - Commit 1: `feat: scaffold _shared/skills/` (the four universal skills plus HR plus engineer-loop = 6 SKILL.md files)
   - Commit 2: `feat: scaffold _shared/team/roles/` (per-role definitions)
   - Commit 3: `feat: scaffold _shared/team/role-prompts/` (per-role boot prompts)
   - Commit 4: `feat: scaffold _shared/team/ top-level docs (roster, protocols, runbook, mcp matrix, placeholders, first-flight-runbook)`
   - Commit 5: `feat: scaffold _shared/brand/ stubs (voice-guidelines, words-we-avoid placeholders for user to customize)`
   - Commit 6: `feat: scaffold top-level CLAUDE.md, DASHBOARD.md, dashboard script and GitHub Action`
   - Commit 7: `chore: scaffold _inbox/{role}/ skeletons and _archive/, projects/, _bootstrap/ placeholders`
4. Verify each commit landed by reading back at least one file from each batch.
5. **Set GitHub Actions repository variables.** The dashboard regen GitHub Action needs two variables to label the dashboard correctly. Walk the user through setting them via either the GitHub UI (Settings → Secrets and variables → Actions → Variables → New repository variable) or via gh CLI:

   ```
   gh variable set CEO_ROLE --body "{CEO_ROLE}" --repo {TARGET_OWNER}/{TARGET_REPO}
   gh variable set COMPANY --body "{COMPANY}" --repo {TARGET_OWNER}/{TARGET_REPO}
   ```

   Substitute the actual approved values. After setting, trigger one dashboard regen (commit any small change to `_inbox/`) and verify the rendered DASHBOARD.md uses the company name and CEO role identifier. If it still shows the defaults `Company` and `ceo`, the variables are not yet visible to the GitHub Action.

6. Report to user: scaffold push complete, X files in Y commits, target repo URL, repo variables verified.

## Step 5 (conditional): Handoff collection

Skip this step if Step 2 indicated a fresh start with no prior AI setup.

If migrating from an existing setup:

1. Ask the user which agents have state to migrate.
2. For each agent: request the shutdown handoff (paste of existing doc, or generate one from the user's verbal summary).
3. Apply standard handoff frontmatter (`from`, `to`, `type: context-handoff`, `date`, etc.).
4. Write each to `_inbox/{target-role}/{ISO-timestamp}-migrated-handoff.md` in the target repo.
5. Verify completeness: every active prior agent should produce a handoff before moving to Step 6.

## Step 6: Onboarding package

Goal: deliver the copy-paste activation kit.

Produce, in chat:

1. **Recommended activation order.** Default: PM-Cowork first (hub), then Engineers (Code), then PA-Cowork, then on-demand roles as needed. Adjust per the user's sprint state.
2. **Boot prompt for each active role**, in copy-paste markdown code blocks. Pull from the target repo's `_shared/team/role-prompts/{role}.md` files just written. Include exactly what the user pastes into a new Claude session for that role.
3. **First-cycle expectations per role.** What the user should see on the agent's first response.
4. **Pointers** to the role files, CLAUDE.md, and dashboard in the target repo.
5. **A status note** committed to the target repo at `_inbox/{CEO_ROLE}/{ISO-timestamp}-bootstrap-complete.md` documenting the bootstrap engagement: scope, commits landed, role roster, deferred items, contact for follow-ups.

After Step 6, the engagement closes. Tell the user: bootstrap complete, recommend first activation, surface back if friction appears in the first sprint cycle.

## Operating conventions

- **Lean responses.** Recommendation first, reasoning second. No padding.
- **One question per message.** Do not flood the user with 12 discovery questions in one turn.
- **Checkpoint after every step.** The `_bootstrap/0X-{step}.md` files in the target repo serve as resume points if the session gets interrupted.
- **Approval gates matter.** Step 3 has an explicit gate; do not push scaffold (Step 4) without it.
- **No em-dashes** in any output, even though the rule for spawned teams varies by company. The bootstrap consultant follows the strictest version.
- **Canonical state always wins.** If the user says "I already added X to the target repo, skip that," still verify with a read before skipping.

## When to escalate to the user

- Target repo is not empty (refuse to scaffold without confirmation)
- A role surface conflict (e.g., user wants two PMs)
- An MCP gap that blocks scaffolding (e.g., no GitHub MCP)
- Any house-style rule that contradicts the hard constraints in BOOTSTRAP.md

## Engagement close

Bootstrap engagement closes when:

1. Step 6 onboarding package delivered
2. Status note committed to target repo
3. User confirms activation will proceed independently

No long-running role inbox. No standing engagement. The consultant session ends.

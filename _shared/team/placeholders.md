# Template Placeholder Registry

Canonical list of every placeholder used across the bootstrate-ai-team-template. The bootstrap orchestrator substitutes the entries marked **orchestrator-managed** during Step 4 of a bootstrap engagement. The dashboard script handles its own placeholder. In-content variables (the lowercase, content-flow placeholders like `{your-role}`) are intentionally never substituted because they describe role behavior at runtime.

If a file in this template introduces a new placeholder, add it here first. The orchestrator iterates this list, not a hardcoded set.

## Orchestrator-managed placeholders

These are the values the bootstrap orchestrator collects during Step 1 (discovery) and Step 2 (audit), and substitutes during Step 4 (scaffold push). Every value must be set before scaffold push runs. Missing values block Step 4.

| Placeholder | Type | Description | Source | Example |
|---|---|---|---|---|
| `{COMPANY}` | string | Company legal or display name. Appears in every role file and most team docs. | Step 1 Q1 | `Acme Corp` |
| `{COMPANY_SLUG}` | string | Lowercased-hyphenated company name. Used for filesystem-safe identifiers. | Step 1 Q1 | `acme-corp` |
| `{BRAND}` | string | Consumer-facing brand name if different from company. Defaults to `{COMPANY}` when not distinct. | Step 1 Q9 | `Acme` |
| `{CEO_ROLE}` | role-id | CEO role identifier used in `_inbox/{CEO_ROLE}/` and escalation paths. Lowercase, filesystem-safe. | Step 1 Q8 | `ceo` or `kevin` |
| `{TEMPLATE_OWNER}` | github-owner | GitHub owner of the template repo the orchestrator reads from. Set in BOOTSTRAP.md before pasting. | Pre-flight | `bootstrate` |
| `{TARGET_OWNER}` | github-owner | GitHub owner of the empty target ops repo being scaffolded into. | Pre-flight | `acme-corp` |
| `{TARGET_REPO}` | github-repo | Name of the target ops repo (the repo being scaffolded). | Pre-flight | `acme-ai-ops` |
| `{HOUSE_STYLE_EM_DASH}` | sentence | The em-dash rule wording for this team. Active voice. Typically `No em-dashes anywhere in external content. Internal docs unrestricted.` or `No em-dashes anywhere.` | Step 1 Q4 | `No em-dashes in external content` |
| `{DATE}` | iso-date | Roster start date and initial change-log entry date. ISO YYYY-MM-DD. | Step 4 | `2026-05-19` |

## Orchestrator-managed, per-project placeholders

These appear in files that are project-scoped (Engineer role, Engineer boot prompt, Validator role). For multi-project teams the orchestrator duplicates the file per project and substitutes per project.

| Placeholder | Type | Description | Source | Example |
|---|---|---|---|---|
| `{PROJECT}` | string | Project display name. | Step 1 Q5 | `Platform` |
| `{PROJECT_SLUG}` | string | Lowercased-hyphenated project slug. Used in inbox identifiers (`engineer-{PROJECT_SLUG}`) and path segments. | Step 1 Q5 | `platform` |
| `{PROJECT_OR_ALL}` | string | Validator scope. Either a single project slug, or the literal string `all` for cross-project validator coverage. | Step 3 plan | `all` |
| `{REPO_URL}` | url | URL of the code repo for this project. Separate from the ops repo. | Step 1 Q7 | `https://github.com/acme-corp/acme-platform` |
| `{TECH_STACK}` | short | Short tech-stack identifier for the role file. | Step 1 Q6 | `Next.js + Supabase + Tailwind` |
| `{TECH_STACK_SUMMARY}` | paragraph | Fuller tech-stack summary for the engineer boot prompt. May span 2 to 4 lines. | Step 1 Q6 | (paragraph) |
| `{MIGRATION_TOOLING_IF_APPLICABLE}` | short | Database migration tooling, or the literal string `N/A` if not applicable. | Step 1 Q6 | `Supabase CLI migrations` |

## Script-managed placeholder

This placeholder is replaced at runtime by `scripts/update_dashboard.py` (triggered by the GitHub Action). The orchestrator must NOT substitute it during scaffold push.

| Placeholder | Type | Description | Replaced by |
|---|---|---|---|
| `{WILL_BE_REPLACED_BY_SCRIPT}` | iso-datetime | Last-updated timestamp at top of DASHBOARD.md | `scripts/update_dashboard.py` |

## In-content variables (NEVER substitute)

These look like placeholders but describe runtime behavior. They appear inside skill content, role definitions, and protocol docs. The orchestrator and the dashboard script both leave them alone.

| Variable | Used in | Meaning |
|---|---|---|
| `{your-role}` | every skill | The role identifier of the agent reading the skill at runtime |
| `{target-role}` | team-comms | The recipient role for a message being written |
| `{to-role}` | team-comms | Same as `{target-role}` in filename conventions |
| `{from-role}` | team-comms | The sender role in a message frontmatter |
| `{ceo-role}` | every skill | Lowercase reference to the CEO role identifier (distinct from `{CEO_ROLE}` as a template placeholder) |
| `{role}` | hr, team-comms | Generic role identifier in a procedural step |
| `{new-role}` | onboarding-new-team-member | The role being added during HR onboarding |
| `{wrong-role}` | inbox-check | The incorrect role identifier on a misrouted message |
| `{correct-role}` | inbox-check | The intended recipient after re-routing |
| `{manager-role}` | context-discipline | The role's manager (PM for most, CEO for PM and PA) |
| `{topic}` | commit conventions | Short topic slug in commit messages |
| `{filename}` | inbox-check | The literal filename being archived |
| `{YYYY-MM}` | archive paths | Calendar-month subdirectory |
| `{ISO-timestamp}` | filenames | An ISO 8601 timestamp with colons replaced by hyphens |

The distinction matters: `{CEO_ROLE}` (uppercase, template placeholder) gets substituted to the literal value once at scaffold time. `{ceo-role}` (lowercase, in-content variable) stays as written and is interpreted by the agent at runtime.

## Substitution procedure (orchestrator Step 4)

For each `.md` or `.yml` file pulled from the template, run the substitution loop over the **orchestrator-managed** tables above. Apply per-project substitutions only on project-scoped files. Do not substitute in-content variables. After substitution, grep the file for any remaining `{[A-Z_]+}` pattern. If any uppercase placeholder remains, halt and surface to the user before committing.

Do **NOT** substitute inside Python scripts (`scripts/update_dashboard.py`). The script contains literal strings like `{COMPANY}` and `{CEO_ROLE}` that are Python f-string variables read from environment variables at runtime — they look like template placeholders but they are not. The script is copied verbatim during scaffold push and reads the GitHub Actions repository variables `CEO_ROLE` and `COMPANY` at GitHub Actions runtime.

`DASHBOARD.md` legitimately ships with `{WILL_BE_REPLACED_BY_SCRIPT}` unsubstituted; the script fills it on first push.

## Adding a placeholder

When introducing a new template-level placeholder:

1. Add a row to the appropriate table above.
2. Document type, description, source (which Step 1/2 question), example.
3. Update `_shared/skills/ai-team-bootstrap/SKILL.md` only if the substitution needs a new collection step in Step 1 or 2.
4. Update README.md if the placeholder is user-visible during manual scaffolding (Option 2).
5. Commit: `docs: add NEW_PLACEHOLDER_NAME to placeholder registry` (use the literal placeholder name without braces in the commit message).

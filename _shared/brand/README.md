# Brand Directory

Holds brand standards for {COMPANY}. Every agent that produces external-facing content reads from here.

## Files

| File | Purpose | Filled by |
|------|---------|-----------|
| `guidelines.md` | Brand voice, tone, personality | Operator at scaffold time |
| `words-we-avoid.md` | Prohibited terms and phrases | Operator at scaffold time |
| `visual-identity.md` | Colors, fonts, logo (used by dashboard) | Operator at scaffold time |
| `bootstrate-defaults.md` | Fallback brand defaults | Ships with template |
| `voice-guidelines.md` | Extended voice guide (legacy stub) | Optional |

## How agents use this

- **Before any external-facing content:** Read `guidelines.md`. If placeholder text only, fall back to Bootstrate default tone (direct, technical, no padding).
- **Before producing copy:** Check `words-we-avoid.md` and filter output.
- **Dashboard script:** Reads `visual-identity.md` frontmatter for CSS variables; falls back to `bootstrate-defaults.md` if unpopulated.

## When to update

After bootstrap, replace placeholder content in `guidelines.md`, `words-we-avoid.md`, and `visual-identity.md`. Commit: `docs: brand {file} customized for {COMPANY}`. Notify PM so agents pick up the change on next read.

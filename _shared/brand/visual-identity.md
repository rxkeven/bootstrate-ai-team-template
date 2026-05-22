---
primary: "#1a1a2e"
accent: "#e94560"
background: "#f8f9fa"
text: "#212529"
surface: "#ffffff"
border: "#dee2e6"
font_family: "Inter, system-ui, sans-serif"
font_family_mono: "JetBrains Mono, monospace"
---

# {COMPANY} Visual Identity (placeholder — fill at scaffold time)

> **Operator:** Replace the frontmatter values above with your real brand colors and fonts. The dashboard script reads these to generate brand-aware HTML. Until replaced, the dashboard falls back to Bootstrate defaults.

## Colors

- `primary` — primary brand color (headers, key UI elements)
- `accent` — highlight / call-to-action color
- `background` — page background
- `text` — body text
- `surface` — card / panel background
- `border` — divider and border color

## Typography

- `font_family` — body font stack (CSS `font-family` value)
- `font_family_mono` — monospace font stack (identifiers, code)

## Logo

*Add `logo_url` to frontmatter if you have a hosted logo URL. Dashboard header uses it if present.*

## Customization

1. Edit the frontmatter values at the top of this file.
2. Commit: `docs: brand visual-identity customized for {COMPANY}`
3. The next dashboard build picks up the new colors and fonts automatically.

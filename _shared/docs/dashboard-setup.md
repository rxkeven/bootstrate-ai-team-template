# Ops Dashboard Setup

6-step guide to deploy the auto-generated ops dashboard to Vercel with access protection.

The dashboard script (`scripts/update_dashboard.py`) generates both `DASHBOARD.md` (for GitHub) and `public/index.html` (for Vercel) on every qualifying push. Vercel serves the `public/` directory.

## Prerequisites

- Scaffold complete; ops repo populated and pushed to GitHub
- GitHub repository connected to Vercel (Vercel imports the repo)
- `COMPANY` and `CEO_ROLE` repo variables set (see Step 4)

## Steps

### 1. Create Vercel project

In the Vercel dashboard, click **Add New Project** and import your ops GitHub repository. When prompted for a framework preset, select **Other**. Vercel reads `vercel.json` at the repo root to configure the deployment (output directory: `public/`, no build command).

### 2. Set GitHub Actions secret

In your GitHub repo: **Settings → Secrets and variables → Actions**, add:

| Secret | Value |
|--------|-------|
| `VERCEL_TOKEN` | Your Vercel API token (Vercel **Account Settings → Tokens**) |

The update-dashboard GitHub Action uses this token to notify Vercel of new deployments after regenerating the dashboard HTML.

### 3. Configure deployment protection

In your Vercel project: **Settings → Deployment Protection**, enable one of:

- **Password protection** — simplest. Set a shared password for the team.
- **Vercel Authentication** — restricts access to Vercel team members.

Do not leave the dashboard public. It surfaces operational state.

### 4. Set repo variables

In your GitHub repo: **Settings → Secrets and variables → Variables**, set:

| Variable | Value |
|----------|-------|
| `COMPANY` | Your company name (used in dashboard header) |
| `CEO_ROLE` | Your CEO's role identifier (used for inbox section label) |

These are read by `scripts/update_dashboard.py` at generation time.

### 5. Push to trigger first build

Push any change to a path covered by the update-dashboard GitHub Action (e.g., any `_inbox/**` change). The GitHub Action:

1. Runs `scripts/update_dashboard.py`
2. Commits updated `DASHBOARD.md` and `public/index.html`
3. The push to `public/` triggers a Vercel deployment

Confirm the Vercel deployment completes and the dashboard URL loads.

### 6. Verify protection is active

Open the dashboard URL in an incognito window. You should be prompted for a password or Vercel authentication before seeing the dashboard. If not, check **Deployment Protection** settings in Vercel.

## Brand customization

The dashboard uses CSS variables derived from `_shared/brand/visual-identity.md` frontmatter. To update colors and fonts:

1. Edit the frontmatter in `_shared/brand/visual-identity.md`
2. Commit and push
3. The workflow regenerates and deploys automatically

## Reference

Vercel implementation reference: vitalhealth-ai-ops.vercel.app

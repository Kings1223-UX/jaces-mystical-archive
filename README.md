# MTG Proxy Studio v0.9 — Hosted database edition

This edition preserves the v0.8 interface and card printing. It automatically loads `cards.json` from the same website. A GitHub Actions workflow checks Scryfall Oracle Cards bulk data daily and deploys the site to GitHub Pages. It needs **no locally installed software**.

## One-time setup (web browser only)

1. Sign in to GitHub and create a new **public** repository (for example `mtg-proxy-studio`).
2. Upload the contents of this ZIP **preserving folders**, including `.github/workflows/update-and-deploy.yml`, `scripts/update_cards.py`, `index.html`, and `README.md`. GitHub's web editor can create each file by typing its full path if folder upload does not preserve `.github`.
3. In repository **Settings → Pages → Build and deployment**, choose **GitHub Actions** as the source.
4. In the repository **Actions** tab, run **Update card database and deploy** using **Run workflow**, or let the push trigger run it. Approve workflows if GitHub asks.
5. Wait for the workflow to complete successfully, then visit `https://YOUR-USERNAME.github.io/mtg-proxy-studio/` (replace with your GitHub username and repository name).

The first workflow run downloads and processes the full Oracle Cards bulk file. Later runs check the upstream `updated_at` value and publish newer data. GitHub scheduled workflows can be delayed or skipped; the site updates after a successful scheduled run, not instantaneously on every Scryfall change. If a run fails, the previously deployed site remains available.

**Important:** GitHub Pages is public hosting. Do not upload personal files, private decklists, or secrets to the repository. Your decklist stays in the browser while using the app; exporting it creates a local text download.

**Fallback:** If the hosted database is unavailable, use Database settings to import your existing Scryfall JSONL file. On a fresh computer, a deployed site with a successful database run should not need this step.

**Limits:** Initial database download can be large. Browser-based PDF print still depends on printer scaling and browser print settings. Automatic updates depend on GitHub Actions remaining enabled and on Scryfall's bulk data endpoint.


## Jace's Mystical Archive shell (v1.0)

The site now includes Home, Codex, Analytics, Collection, and Proxy navigation. Only Proxy is functional; the other sections are intentionally labeled placeholders. Loot's bell has a notification inbox UI but no AI backend or live messaging yet. Settings is also a placeholder. Proxy card text boxes have subtle shadows, and mana/color identifiers use U for blue and B for black. Existing GitHub Actions database workflow is retained.

## v1.1 typography and color

- All four white template sections have a faint outline in addition to the existing drop shadow.
- Name, type and rules fields shrink their fonts to fit their rendered bounds (down to a legibility floor). Cards with unusually long text may still require manual review.
- Oracle keyword ability lines are bold; reminder text in parentheses and recognized ability-word labels are italicized. Text content is not rewritten.
- Power/toughness uses larger bold type.
- Black mana identifier `B` is now rendered as a lighter lilac purple (`#B89AD9`) for better contrast against blue `U`. This is a deliberate visual override of the earlier CMYK approximation.

The app's browser print flow and Scryfall database workflow are unchanged.

# orbitalml — Design Spec

> **Rename note (2026-04-19):** This platform was originally named "Planet Harness" during brainstorming; renamed to **orbitalml** after the GitHub repo was created at `orbit-ml/orbitalml`. File names preserved for history; content updated throughout. Tagline is pending final user confirmation.

**Date:** 2026-04-19
**Status:** Draft, pending implementation plan

## Purpose

orbitalml is the interactive showcase site for the `orbit4ml` open-source library. It serves two aligned goals:

1. **CSR mission** — Lower the activation energy for anyone curious about ML in space. No install, no signup, instant interactivity.
2. **Commercial pipeline** — Signal credibility and capture leads for the space ML runtime company the user is building around `orbit4ml`.

The site is a **marketing/learning asset, not a SaaS.** No accounts, no compute-backed submissions, no self-hosted forum.

## Name and Tagline

- **Name:** orbitalml
- **Tagline (H1 on hero):** *ML harness for the planet.*
- **Sub-copy:** "Interactive tutorials, benchmarks, and playgrounds for machine learning under the real constraints of space. No install required."

## Relationship to Existing orbit4ml Docs

- **orbitalml** (new) — The "front door." Hero, tutorials, playground, blog, benchmarks, lead capture.
- **orbit4ml MkDocs site** (existing, at `orbit-ml.github.io/orbit4ml`) — Stays as the auto-generated API reference. orbitalml's "Docs" nav links out to it.

Two sites, one visual identity. Future work may unify them, but that's out of scope for v1.

## Visual Direction

Blend of "cosmic/immersive" and "technical minimalist." Dark, polished, undeniably space.

- **Background:** `#0a0e18` (deep space, cooler than pure black)
- **Primary text:** `#f0f3fa`
- **Secondary text:** `#9aa3b8`
- **Accent gradient:** `#7aaeff` → `#c3a6ff` (blue → purple)
- **Typography:** Inter 400–600 for body and headings (letter-spacing -0.5px on large headings); JetBrains Mono 10–11px for micro-labels, stats, telemetry strips
- **Motifs:** Subtle low-opacity starfield, orbital-ring visualizations, floating telemetry tooltips (e.g., `SAT 23 · power: ok · thermal: ok`), thin 1px borders `rgba(255,255,255,0.06)`
- **Hero visualization:** Animated 3D(ish) constellation — Earth with orbital rings, satellite dots cycling through eclipse/sunlit states in real time

## Top-Level Sections

All seven confirmed during brainstorming.

1. **Learn** — Interactive guided tutorials. Editable, runnable Python cells inline. The "excitement" engine.
2. **Playground** — Free-form in-browser notebook, pre-loaded with `orbit4ml`. For users who want to explore without a script.
3. **Docs** — External link to the MkDocs API reference.
4. **Blog / Case Studies** — Thought leadership. Benchmark deep-dives, "how we ran X on orbit" stories. Drives the commercial pipeline.
5. **Benchmarks** — Published performance numbers (curated by the team, not user submissions). Credibility signal.
6. **For Missions** — Commercial teaser page for the runtime company. Newsletter signup + contact capture for leads (satellite operators, agencies, primes).
7. **Community** — Links out to GitHub Discussions, contributor list. No self-hosted forum.

## Interactive Tutorial Approach (Blend)

Different tech for different surfaces — each picked for the best UX at that surface.

| Surface | Tech | Why |
|---------|------|-----|
| **Learn** (guided tutorials) | **Pyodide** (embedded code cells on each page) | In-page, polished, edit-and-run inline. Pure-Python orbit4ml.sim works fine; torch swapped for web-friendly stand-ins where needed. |
| **Playground** (free-form) | **JupyterLite** | Full notebook UI for exploratory work. Heavy but correct tool for the job. |
| **Heavy torch examples** | **"Open in Colab"** escape hatch | Zero-cost, full GPU access. Users leave the site, but they get working training runs. |

`orbit4ml` itself is pure Python (sgp4 is pure Python); the lightweight training loop examples use small models. Heavy examples (`EuroSAT + CNN`) get a "Try in Colab" button rather than being forced through Pyodide.

## Tech Stack

- **Framework:** **Astro** — Ships zero JS by default, supports React/Svelte "islands" for interactive pieces (code runner, 3D constellation viz, animations), first-class MDX for tutorials and blog.
- **Hosting:** **Vercel** — Excellent DX, preview deploys on every PR, easy custom domain and SSL.
- **Interactive islands:** React (largest component ecosystem for the pieces we need — Pyodide REPL UI, 3D viz via `react-three-fiber` / `three.js`).
- **Content:** MDX for tutorials and blog posts. Authored in the repo, reviewed via PR.
- **Code execution:** Pyodide 0.x (latest stable) loaded on-demand per page; JupyterLite hosted for the Playground surface.
- **Lead capture:** Newsletter via **Buttondown** or **ConvertKit** (hosted, no infra). "For Missions" contact form via **Formspree** or Vercel serverless function posting to email.
- **Analytics:** **Plausible** (privacy-friendly, no cookie banner) or Vercel Analytics.
- **Repo layout:** Standalone `orbitalml` repo (separate from `orbit4ml` library repo). Library consumed via its documented public API.

## Architecture Outline

```
orbitalml/
├── astro.config.mjs
├── src/
│   ├── pages/
│   │   ├── index.astro          # Hero + feature grid
│   │   ├── learn/
│   │   │   ├── index.astro      # Tutorial index
│   │   │   └── [...slug].astro  # Dynamic MDX-rendered tutorials
│   │   ├── playground.astro     # JupyterLite embed
│   │   ├── blog/
│   │   │   └── [...slug].astro
│   │   ├── benchmarks.astro
│   │   ├── missions.astro       # "For Missions" lead capture
│   │   └── community.astro
│   ├── components/
│   │   ├── Hero.astro
│   │   ├── Nav.astro
│   │   ├── Footer.astro
│   │   ├── ConstellationViz.tsx # React island, three.js
│   │   ├── CodeRunner.tsx       # React island, Pyodide
│   │   └── NewsletterSignup.tsx # React island
│   ├── content/
│   │   ├── tutorials/           # .mdx tutorial files
│   │   └── blog/                # .mdx blog posts
│   ├── layouts/
│   └── styles/
│       └── tokens.css           # design tokens (colors, spacing)
└── public/
    └── pyodide/                 # pinned Pyodide + wheels
```

Each module is one thing:
- `ConstellationViz` — renders the orbital visualization; consumer passes satellite data
- `CodeRunner` — standalone Pyodide-backed code cell; reusable inside any MDX tutorial
- `NewsletterSignup` — posts to Buttondown/ConvertKit; used in hero, footer, blog posts

## What's In Scope (v1)

- Homepage with hero, feature grid, newsletter signup
- Learn section: **3 starter tutorials** (Getting Started, Simulating a Constellation, Training Under Eclipse)
- Playground section: JupyterLite embed with `orbit4ml` pre-installed
- Blog with 1–2 launch posts
- Benchmarks page: published numbers from the `orbit4ml` MVP (70% training utilization, etc.)
- "For Missions" page with contact form and newsletter
- Community page with GitHub Discussions embed/link
- Mobile-responsive (breakpoints: 640px, 1024px)
- Dark theme only (no light mode for v1)
- Custom domain: `orbitalml.com` (user to register)

## What's Out of Scope (v1, defer explicitly)

- User accounts / login
- Progress tracking per user
- Auto-graded exercises
- User-submitted benchmark runs (compute backend)
- Self-hosted forum
- Multi-language support
- Certificates / badges
- Offline mode

Each of these is a legitimate future addition, but shipping v1 without them is explicit — they are not oversights.

## Testing

- **Visual regression:** Playwright screenshot tests on key pages (hero, a tutorial, playground) at 3 breakpoints
- **Pyodide smoke:** A Playwright test that loads `/learn/getting-started`, runs the first code cell, and asserts the expected output appears
- **Build:** `astro check` + `astro build` in CI on every PR
- **Link checker:** Lychee or similar in CI to catch broken internal/external links
- **Lighthouse CI:** Score budgets on the homepage (Performance ≥ 90, Accessibility ≥ 95)

## Success Criteria

- **CSR lens:** Visitor lands, reads the hero, clicks "Try in browser," and runs their first satellite simulation **without installing anything** in under 60 seconds of attention
- **Commercial lens:** "For Missions" page captures ≥ 5 qualified inbound leads/month within 3 months of launch (placeholder target — revise once baseline traffic is known)
- **Quality lens:** Lighthouse ≥ 90 on homepage, first tutorial loads and executes first code cell in < 8s on a cold cache, passes Playwright smoke test on every main-branch commit
- **SEO lens:** Ranked on first page for "machine learning in space", "orbital ML", "satellite ML tutorial" within 6 months

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Pyodide bundle size hurts first-paint | Lazy-load on tutorial pages only; hero is static |
| Torch unavailable in Pyodide | Use Colab escape hatch for torch-heavy examples; keep Pyodide tutorials to `orbit4ml.sim` (pure Python) |
| Commercial teaser page feels salesy, damages CSR credibility | Keep "For Missions" understated; frame as "get in touch" not "buy now"; no popups, no dark patterns |
| Two repos (library + site) drift | Library version pinned in site package.json notes; site CI pulls latest released library |
| Custom domain renewal / DNS | Document domain registrar and DNS records in repo README |

## Non-Goals

- Replacing the MkDocs API reference (it stays; orbitalml links to it)
- Replacing GitHub Discussions with a self-hosted forum
- Building a full LMS
- Competing with Kaggle / Hugging Face Spaces — orbitalml is specialized for space ML, not a general platform

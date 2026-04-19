# orbitalml v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship v1 of orbitalml — the interactive showcase site for orbit4ml at `orbitalml.com`. Homepage, 3 Learn tutorials with in-browser Python, JupyterLite playground, blog, benchmarks, For Missions lead capture, Community page. Dark theme, mobile-responsive.

**Architecture:** Astro static site with React islands for interactive pieces (CodeRunner/Pyodide, ConstellationViz/three.js, NewsletterSignup). MDX for tutorials and blog. Content collections for typed authoring. Vercel for hosting + preview deploys + serverless contact form. Playwright + Lighthouse CI for quality gates.

**Tech Stack:** Astro 4.x, TypeScript, React 18, react-three-fiber, Pyodide 0.25+, JupyterLite, Buttondown (newsletter), Formspree (contact), Plausible (analytics), Playwright, Vercel.

---

## Prerequisites

**Before starting task 1, the human must:**

1. Create an empty GitHub repo at `https://github.com/orbit-ml/orbitalml` (public, no README, no .gitignore, no license — these will be committed from Task 1)
2. Create the local project directory: `mkdir C:/Users/mmallick7/orbitalml`
3. Initialize it with the remote: `cd C:/Users/mmallick7/orbitalml && git init && git remote add origin https://github.com/orbit-ml/orbitalml.git`

All tasks below are executed inside `C:/Users/mmallick7/orbitalml/` unless noted.

**Third-party account setup (do as reached — not blocking Task 1):**

- **Vercel** — connect to the GitHub repo once Task 32 starts
- **Buttondown** — create account, grab API key, set env var `BUTTONDOWN_API_KEY` (see Task 11)
- **Formspree** — create a form for contact, grab form ID, set env var `FORMSPREE_FORM_ID` (see Task 30)
- **Plausible** — create site for `orbitalml.com`, grab script snippet (see Task 32)

---

## Phase 1: Foundation

### Task 1: Bootstrap Astro project

**Files:**
- Create: `package.json`, `astro.config.mjs`, `tsconfig.json`, `.gitignore`, `README.md`, `LICENSE`

- [ ] **Step 1: Run Astro scaffold**

```bash
cd C:/Users/mmallick7/orbitalml
npm create astro@latest . -- --template minimal --typescript strict --no-install --no-git --yes
```

Expected: creates `src/`, `public/`, `package.json`, `astro.config.mjs`, `tsconfig.json`.

- [ ] **Step 2: Install dependencies**

```bash
npm install
npm install -D @astrojs/react @astrojs/mdx @astrojs/sitemap @astrojs/check typescript
npm install react@18 react-dom@18
```

Expected: `node_modules/` populated, `package-lock.json` created.

- [ ] **Step 3: Configure Astro integrations**

Overwrite `astro.config.mjs`:

```js
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://orbitalml.com',
  integrations: [react(), mdx(), sitemap()],
  trailingSlash: 'never',
});
```

- [ ] **Step 4: Replace README and add LICENSE**

Overwrite `README.md`:

```markdown
# orbitalml

The interactive showcase site for [orbit4ml](https://github.com/orbit-ml/orbit4ml).

> ML harness for the planet.

## Develop

```bash
npm install
npm run dev
```

## Build

```bash
npm run build   # outputs to ./dist
```

## Deploy

Automatic via Vercel on push to `main`.
```

Create `LICENSE` (MIT, same as orbit4ml — copy from that repo or generate):

```
MIT License

Copyright (c) 2026 Mainak Mallick

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 5: Verify build**

```bash
npm run build
```

Expected: `✔ Completed in ~Xs. Building client routes...` with 0 errors. A `dist/` directory is created.

- [ ] **Step 6: Commit**

```bash
git add .
git commit -m "chore: bootstrap Astro + React + MDX project"
git branch -M main
git push -u origin main
```

---

### Task 2: Design tokens and global styles

**Files:**
- Create: `src/styles/tokens.css`, `src/styles/global.css`

- [ ] **Step 1: Write the design-token stylesheet**

Create `src/styles/tokens.css`:

```css
:root {
  /* Colors */
  --color-bg: #0a0e18;
  --color-bg-elevated: #0f1524;
  --color-text-primary: #f0f3fa;
  --color-text-secondary: #9aa3b8;
  --color-text-muted: #6a7590;
  --color-accent-blue: #7aaeff;
  --color-accent-purple: #c3a6ff;
  --color-accent-gradient: linear-gradient(90deg, #7aaeff 0%, #c3a6ff 100%);
  --color-border: rgba(255, 255, 255, 0.06);
  --color-border-strong: rgba(255, 255, 255, 0.14);
  --color-success: #7fff7f;
  --color-warning: #ffae7a;

  /* Spacing scale (multiples of 4px) */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;
  --space-20: 80px;

  /* Typography */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', Consolas, monospace;

  /* Radii */
  --radius-sm: 3px;
  --radius-md: 4px;
  --radius-lg: 8px;
  --radius-full: 9999px;

  /* Breakpoints (used in media queries, not as CSS vars) */
  /* sm: 640px, md: 1024px, lg: 1280px */
}
```

- [ ] **Step 2: Write global stylesheet**

Create `src/styles/global.css`:

```css
@import './tokens.css';

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after {
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  background: var(--color-bg);
  color: var(--color-text-primary);
  font-family: var(--font-sans);
  font-size: 14px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

a {
  color: inherit;
  text-decoration: none;
}

a:hover {
  color: var(--color-accent-blue);
}

h1, h2, h3, h4 {
  font-weight: 600;
  letter-spacing: -0.5px;
  margin: 0 0 var(--space-4) 0;
}

h1 { font-size: 40px; line-height: 1.05; letter-spacing: -1px; }
h2 { font-size: 28px; line-height: 1.15; }
h3 { font-size: 20px; line-height: 1.25; }

p {
  margin: 0 0 var(--space-4) 0;
  color: var(--color-text-secondary);
}

code {
  font-family: var(--font-mono);
  font-size: 0.9em;
  background: var(--color-bg-elevated);
  padding: 2px 6px;
  border-radius: var(--radius-sm);
}

pre {
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  overflow-x: auto;
}

pre code {
  background: transparent;
  padding: 0;
}

.mono {
  font-family: var(--font-mono);
}

.micro-label {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 2.5px;
  color: var(--color-accent-blue);
  text-transform: uppercase;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--space-6);
}
```

- [ ] **Step 3: Commit**

```bash
git add src/styles/
git commit -m "style: add design tokens and global stylesheet"
git push
```

---

### Task 3: Base Layout component

**Files:**
- Create: `src/layouts/BaseLayout.astro`

- [ ] **Step 1: Write the base layout**

Create `src/layouts/BaseLayout.astro`:

```astro
---
import '../styles/global.css';
import Nav from '../components/Nav.astro';
import Footer from '../components/Footer.astro';

export interface Props {
  title: string;
  description?: string;
  ogImage?: string;
}

const {
  title,
  description = 'ML harness for the planet. Interactive tutorials, benchmarks, and playgrounds for machine learning in space.',
  ogImage = '/og-default.png',
} = Astro.props;

const fullTitle = title === 'orbitalml' ? title : `${title} · orbitalml`;
const canonical = new URL(Astro.url.pathname, Astro.site).href;
---

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="color-scheme" content="dark" />
    <title>{fullTitle}</title>
    <meta name="description" content={description} />
    <link rel="canonical" href={canonical} />
    <meta property="og:title" content={fullTitle} />
    <meta property="og:description" content={description} />
    <meta property="og:type" content="website" />
    <meta property="og:url" content={canonical} />
    <meta property="og:image" content={new URL(ogImage, Astro.site).href} />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  </head>
  <body>
    <Nav />
    <main><slot /></main>
    <Footer />
  </body>
</html>
```

- [ ] **Step 2: Create placeholder favicon**

Create `public/favicon.svg`:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <circle cx="16" cy="16" r="12" fill="none" stroke="#7aaeff" stroke-width="2"/>
  <circle cx="16" cy="16" r="4" fill="#7aaeff"/>
</svg>
```

- [ ] **Step 3: Commit**

```bash
git add src/layouts/BaseLayout.astro public/favicon.svg
git commit -m "feat: add base layout with SEO meta and slot"
git push
```

---

### Task 4: Nav component

**Files:**
- Create: `src/components/Nav.astro`

- [ ] **Step 1: Write Nav**

Create `src/components/Nav.astro`:

```astro
---
const navItems = [
  { label: 'Learn', href: '/learn' },
  { label: 'Playground', href: '/playground' },
  { label: 'Docs', href: 'https://orbit-ml.github.io/orbit4ml/', external: true },
  { label: 'Blog', href: '/blog' },
  { label: 'Benchmarks', href: '/benchmarks' },
  { label: 'For Missions', href: '/missions' },
  { label: 'Community', href: '/community' },
];
const pathname = Astro.url.pathname;
---

<header class="nav">
  <div class="container nav-inner">
    <a href="/" class="brand" aria-label="orbitalml home">
      <span class="brand-mark" aria-hidden="true"></span>
      <span class="brand-name">orbitalml</span>
    </a>
    <nav aria-label="Primary">
      <ul class="nav-links">
        {navItems.map((item) => (
          <li>
            <a
              href={item.href}
              class:list={['nav-link', { active: !item.external && pathname.startsWith(item.href) }]}
              target={item.external ? '_blank' : undefined}
              rel={item.external ? 'noopener noreferrer' : undefined}
            >
              {item.label}{item.external ? ' ↗' : ''}
            </a>
          </li>
        ))}
        <li>
          <a
            href="https://github.com/orbit-ml/orbit4ml"
            target="_blank"
            rel="noopener noreferrer"
            class="nav-link"
          >GitHub ↗</a>
        </li>
      </ul>
    </nav>
  </div>
</header>

<style>
  .nav {
    position: sticky;
    top: 0;
    z-index: 50;
    background: rgba(10, 14, 24, 0.85);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--color-border);
  }
  .nav-inner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 18px var(--space-6);
  }
  .brand {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 600;
    color: var(--color-text-primary);
    letter-spacing: -0.2px;
  }
  .brand-mark {
    width: 18px;
    height: 18px;
    border: 1.5px solid var(--color-accent-blue);
    border-radius: 50%;
    position: relative;
  }
  .brand-mark::after {
    content: '';
    position: absolute;
    inset: 5px;
    background: var(--color-accent-blue);
    border-radius: 50%;
  }
  .nav-links {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    gap: 22px;
    font-size: 12px;
  }
  .nav-link {
    color: var(--color-text-secondary);
    transition: color 0.15s;
  }
  .nav-link:hover,
  .nav-link.active {
    color: var(--color-text-primary);
  }
  @media (max-width: 1024px) {
    .nav-links {
      display: none;
    }
  }
</style>
```

- [ ] **Step 2: Verify with dev server**

```bash
npm run dev
```

Expected: server starts at `http://localhost:4321`. Nav is not yet visible because there's no index page using `BaseLayout`. Stop the server (Ctrl+C).

- [ ] **Step 3: Commit**

```bash
git add src/components/Nav.astro
git commit -m "feat: add sticky nav with brand mark and links"
git push
```

---

### Task 5: Footer component

**Files:**
- Create: `src/components/Footer.astro`

- [ ] **Step 1: Write Footer**

Create `src/components/Footer.astro`:

```astro
---
const year = new Date().getFullYear();
---

<footer class="footer">
  <div class="container footer-inner">
    <div class="footer-col">
      <div class="footer-brand">orbitalml</div>
      <p class="footer-tagline">ML harness for the planet.</p>
      <p class="footer-meta">Powered by <a href="https://github.com/orbit-ml/orbit4ml">orbit4ml</a> · MIT License</p>
    </div>
    <div class="footer-col">
      <div class="micro-label">Explore</div>
      <ul>
        <li><a href="/learn">Learn</a></li>
        <li><a href="/playground">Playground</a></li>
        <li><a href="/benchmarks">Benchmarks</a></li>
        <li><a href="/blog">Blog</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <div class="micro-label">Engage</div>
      <ul>
        <li><a href="/missions">For Missions</a></li>
        <li><a href="/community">Community</a></li>
        <li><a href="https://github.com/orbit-ml/orbit4ml/discussions" target="_blank" rel="noopener noreferrer">Discussions ↗</a></li>
        <li><a href="https://github.com/orbit-ml/orbit4ml" target="_blank" rel="noopener noreferrer">GitHub ↗</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <div class="micro-label">Resources</div>
      <ul>
        <li><a href="https://orbit-ml.github.io/orbit4ml/" target="_blank" rel="noopener noreferrer">API Docs ↗</a></li>
        <li><a href="/blog">Case Studies</a></li>
      </ul>
    </div>
  </div>
  <div class="container footer-bottom">
    <span>© {year} orbitalml</span>
    <span class="mono">v1.0</span>
  </div>
</footer>

<style>
  .footer {
    margin-top: var(--space-20);
    border-top: 1px solid var(--color-border);
    padding-top: var(--space-12);
    padding-bottom: var(--space-8);
  }
  .footer-inner {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr;
    gap: var(--space-8);
  }
  .footer-brand {
    font-weight: 600;
    margin-bottom: var(--space-2);
  }
  .footer-tagline {
    color: var(--color-text-secondary);
    margin-bottom: var(--space-3);
  }
  .footer-meta {
    font-size: 12px;
    color: var(--color-text-muted);
  }
  .footer-col ul {
    list-style: none;
    padding: 0;
    margin: var(--space-3) 0 0 0;
  }
  .footer-col li {
    margin-bottom: var(--space-2);
    font-size: 13px;
  }
  .footer-col a {
    color: var(--color-text-secondary);
  }
  .footer-col a:hover {
    color: var(--color-text-primary);
  }
  .footer-bottom {
    display: flex;
    justify-content: space-between;
    margin-top: var(--space-8);
    padding-top: var(--space-6);
    border-top: 1px solid var(--color-border);
    font-size: 12px;
    color: var(--color-text-muted);
  }
  @media (max-width: 1024px) {
    .footer-inner { grid-template-columns: 1fr 1fr; }
  }
  @media (max-width: 640px) {
    .footer-inner { grid-template-columns: 1fr; }
  }
</style>
```

- [ ] **Step 2: Commit**

```bash
git add src/components/Footer.astro
git commit -m "feat: add footer with columns and meta strip"
git push
```

---

## Phase 2: Homepage

### Task 6: ConstellationViz React island (three.js)

**Files:**
- Create: `src/components/ConstellationViz.tsx`

- [ ] **Step 1: Install three.js deps**

```bash
npm install three @react-three/fiber @react-three/drei
npm install -D @types/three
```

- [ ] **Step 2: Write the viz component**

Create `src/components/ConstellationViz.tsx`:

```tsx
import { Canvas, useFrame } from '@react-three/fiber';
import { Suspense, useMemo, useRef } from 'react';
import * as THREE from 'three';

const EARTH_RADIUS = 1.0;
const ORBIT_ALTITUDE = 0.7; // relative to earth radius — visual, not physical
const NUM_SATELLITES = 12;

function Earth() {
  const ref = useRef<THREE.Mesh>(null);
  useFrame((_, delta) => {
    if (ref.current) ref.current.rotation.y += delta * 0.05;
  });
  return (
    <mesh ref={ref}>
      <sphereGeometry args={[EARTH_RADIUS, 48, 48]} />
      <meshStandardMaterial
        color="#1a3a7a"
        emissive="#3d7cd9"
        emissiveIntensity={0.12}
        roughness={0.9}
      />
    </mesh>
  );
}

function OrbitRing({ tilt = 0, roll = 0 }: { tilt?: number; roll?: number }) {
  const points = useMemo(() => {
    const pts: THREE.Vector3[] = [];
    const r = EARTH_RADIUS + ORBIT_ALTITUDE;
    for (let i = 0; i <= 100; i++) {
      const theta = (i / 100) * Math.PI * 2;
      pts.push(new THREE.Vector3(Math.cos(theta) * r, 0, Math.sin(theta) * r));
    }
    return pts;
  }, []);
  const geo = useMemo(() => new THREE.BufferGeometry().setFromPoints(points), [points]);
  return (
    <line rotation={[tilt, roll, 0]}>
      <primitive object={geo} attach="geometry" />
      <lineBasicMaterial color="#7aaeff" transparent opacity={0.25} />
    </line>
  );
}

function Satellite({ phase, tilt, roll, color }: { phase: number; tilt: number; roll: number; color: string }) {
  const ref = useRef<THREE.Mesh>(null);
  const rotationQ = useMemo(() => new THREE.Quaternion().setFromEuler(new THREE.Euler(tilt, roll, 0)), [tilt, roll]);
  useFrame((state) => {
    if (!ref.current) return;
    const t = state.clock.elapsedTime * 0.3 + phase;
    const r = EARTH_RADIUS + ORBIT_ALTITUDE;
    const p = new THREE.Vector3(Math.cos(t) * r, 0, Math.sin(t) * r);
    p.applyQuaternion(rotationQ);
    ref.current.position.copy(p);
  });
  return (
    <mesh ref={ref}>
      <sphereGeometry args={[0.035, 12, 12]} />
      <meshBasicMaterial color={color} />
    </mesh>
  );
}

function Stars() {
  const positions = useMemo(() => {
    const arr = new Float32Array(600 * 3);
    for (let i = 0; i < 600; i++) {
      const r = 12 + Math.random() * 6;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      arr[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      arr[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      arr[i * 3 + 2] = r * Math.cos(phi);
    }
    return arr;
  }, []);
  const geo = useMemo(() => {
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    return g;
  }, [positions]);
  return (
    <points>
      <primitive object={geo} attach="geometry" />
      <pointsMaterial color="#ffffff" size={0.03} transparent opacity={0.55} />
    </points>
  );
}

export default function ConstellationViz() {
  const orbits = [
    { tilt: 0.1, roll: 0 },
    { tilt: 0.6, roll: 0.4 },
    { tilt: -0.3, roll: 0.9 },
  ];
  return (
    <Canvas camera={{ position: [0, 1.2, 3.4], fov: 45 }} style={{ width: '100%', height: '100%' }}>
      <Suspense fallback={null}>
        <ambientLight intensity={0.4} />
        <directionalLight position={[5, 3, 5]} intensity={1.2} />
        <Stars />
        <Earth />
        {orbits.map((o, i) => <OrbitRing key={i} tilt={o.tilt} roll={o.roll} />)}
        {Array.from({ length: NUM_SATELLITES }).map((_, i) => {
          const orbit = orbits[i % orbits.length];
          const color = i % 3 === 0 ? '#c3a6ff' : '#7aaeff';
          return (
            <Satellite
              key={i}
              phase={(i / NUM_SATELLITES) * Math.PI * 2}
              tilt={orbit.tilt}
              roll={orbit.roll}
              color={color}
            />
          );
        })}
      </Suspense>
    </Canvas>
  );
}
```

- [ ] **Step 3: Verify it compiles**

```bash
npx astro check
```

Expected: 0 errors, 0 warnings (type-check passes).

- [ ] **Step 4: Commit**

```bash
git add src/components/ConstellationViz.tsx package.json package-lock.json
git commit -m "feat: add ConstellationViz React island with three.js"
git push
```

---

### Task 7: Hero component with embedded viz

**Files:**
- Create: `src/components/Hero.astro`

- [ ] **Step 1: Write Hero**

Create `src/components/Hero.astro`:

```astro
---
import ConstellationViz from './ConstellationViz.tsx';
---

<section class="hero">
  <div class="container hero-inner">
    <div class="hero-copy">
      <div class="micro-label">POWERED BY ORBIT4ML · OPEN SOURCE · MIT</div>
      <h1 class="hero-headline">
        <span class="gradient">ML harness<br />for the planet.</span>
      </h1>
      <p class="hero-sub">
        Interactive tutorials, benchmarks, and playgrounds for machine learning
        under the real constraints of space. No install required.
      </p>
      <div class="hero-ctas">
        <a href="/learn/getting-started" class="btn btn-primary">Try in browser →</a>
        <a href="https://github.com/orbit-ml/orbit4ml" target="_blank" rel="noopener noreferrer" class="btn btn-ghost">
          <span class="mono">pip install orbit4ml</span>
        </a>
      </div>
      <div class="hero-stats">
        <div><span class="stat-val">66</span> sats simulated</div>
        <div><span class="stat-val">70.4%</span> train util</div>
        <div><span class="stat-val">MIT</span> license</div>
      </div>
    </div>
    <div class="hero-viz">
      <ConstellationViz client:visible />
      <div class="tooltip tooltip-top-right">
        <div class="tooltip-label blue">SAT 23</div>
        <div>power: <span class="ok">ok</span></div>
        <div>thermal: <span class="ok">ok</span></div>
      </div>
      <div class="tooltip tooltip-bottom-left">
        <div class="tooltip-label purple">SAT 41</div>
        <div>eclipse · <span class="warn">idle</span></div>
      </div>
    </div>
  </div>
</section>

<style>
  .hero {
    position: relative;
    min-height: 560px;
    padding-top: var(--space-12);
    padding-bottom: var(--space-16);
    overflow: hidden;
  }
  .hero-inner {
    display: grid;
    grid-template-columns: 1.2fr 1fr;
    gap: var(--space-10);
    align-items: center;
  }
  .hero-headline {
    font-size: 48px;
    line-height: 1.03;
    letter-spacing: -1.4px;
    margin: var(--space-4) 0 var(--space-5);
  }
  .gradient {
    background: linear-gradient(90deg, #f0f3fa 0%, #7aaeff 60%, #c3a6ff 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
  }
  .hero-sub {
    color: var(--color-text-secondary);
    font-size: 15px;
    line-height: 1.55;
    max-width: 420px;
    margin-bottom: var(--space-6);
  }
  .hero-ctas {
    display: flex;
    gap: var(--space-3);
    margin-bottom: var(--space-8);
  }
  .btn {
    display: inline-block;
    padding: 10px 20px;
    font-size: 13px;
    font-weight: 500;
    border-radius: var(--radius-md);
    transition: transform 0.1s, background 0.15s;
  }
  .btn-primary {
    background: var(--color-text-primary);
    color: var(--color-bg);
    font-weight: 600;
  }
  .btn-primary:hover { background: var(--color-accent-blue); color: var(--color-bg); }
  .btn-ghost {
    border: 1px solid var(--color-border-strong);
    color: var(--color-text-primary);
  }
  .btn-ghost:hover { border-color: var(--color-accent-blue); }
  .hero-stats {
    display: flex;
    gap: var(--space-6);
    padding-top: var(--space-5);
    border-top: 1px solid var(--color-border);
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--color-text-muted);
  }
  .stat-val { color: var(--color-text-primary); }
  .hero-viz {
    position: relative;
    min-height: 420px;
  }
  .tooltip {
    position: absolute;
    background: rgba(15, 20, 35, 0.85);
    border: 1px solid rgba(122, 174, 255, 0.25);
    padding: 6px 10px;
    border-radius: var(--radius-md);
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--color-text-secondary);
    backdrop-filter: blur(4px);
    pointer-events: none;
  }
  .tooltip-top-right { top: 8%; right: -4px; }
  .tooltip-bottom-left { bottom: 14%; left: -8px; border-color: rgba(195, 166, 255, 0.25); }
  .tooltip-label { font-weight: 500; letter-spacing: 1px; }
  .tooltip-label.blue { color: var(--color-accent-blue); }
  .tooltip-label.purple { color: var(--color-accent-purple); }
  .ok { color: var(--color-success); }
  .warn { color: var(--color-warning); }
  @media (max-width: 1024px) {
    .hero-inner { grid-template-columns: 1fr; }
    .hero-viz { min-height: 320px; }
    .hero-headline { font-size: 36px; }
  }
</style>
```

- [ ] **Step 2: Commit**

```bash
git add src/components/Hero.astro
git commit -m "feat: add hero section with ConstellationViz and telemetry tooltips"
git push
```

---

### Task 8: Feature grid section

**Files:**
- Create: `src/components/FeatureGrid.astro`

- [ ] **Step 1: Write the grid**

Create `src/components/FeatureGrid.astro`:

```astro
---
const features = [
  {
    title: 'Simulate orbital constraints',
    body: 'SGP4 propagation, eclipse modeling, thermal budgets, inter-satellite links, stochastic faults — run a realistic digital twin of a constellation in seconds.',
    href: '/learn/simulating-a-constellation',
    cta: 'Run it in browser →',
  },
  {
    title: 'Train under eclipse',
    body: 'Gate PyTorch training loops on power and thermal state. Watch satellites cycle between sunlit and eclipse, and see how utilization lands at ~70%.',
    href: '/learn/training-under-eclipse',
    cta: 'Try the tutorial →',
  },
  {
    title: 'Benchmark, publish, repeat',
    body: 'Published performance numbers against real space-ML workloads. See what\'s possible with today\'s orbit4ml and where the ceiling is.',
    href: '/benchmarks',
    cta: 'See benchmarks →',
  },
  {
    title: 'For missions',
    body: 'Running ML on a real mission? We\'re building a commercial runtime for radiation-hardened space hardware. Get in touch.',
    href: '/missions',
    cta: 'Talk to us →',
  },
];
---

<section class="features">
  <div class="container">
    <div class="section-head">
      <div class="micro-label">WHAT YOU CAN DO TODAY</div>
      <h2>Run real space ML, in your browser.</h2>
    </div>
    <div class="grid">
      {features.map((f) => (
        <a class="card" href={f.href}>
          <h3>{f.title}</h3>
          <p>{f.body}</p>
          <span class="cta">{f.cta}</span>
        </a>
      ))}
    </div>
  </div>
</section>

<style>
  .features { padding: var(--space-16) 0; }
  .section-head { margin-bottom: var(--space-10); }
  .section-head h2 { max-width: 640px; margin-top: var(--space-3); }
  .grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--space-5);
  }
  .card {
    display: block;
    padding: var(--space-6);
    background: var(--color-bg-elevated);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    transition: border-color 0.15s, transform 0.15s;
  }
  .card:hover {
    border-color: var(--color-accent-blue);
    transform: translateY(-2px);
    color: var(--color-text-primary);
  }
  .card h3 { color: var(--color-text-primary); margin-bottom: var(--space-3); }
  .card p { font-size: 13px; margin-bottom: var(--space-4); }
  .cta {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--color-accent-blue);
    letter-spacing: 0.5px;
  }
  @media (max-width: 640px) { .grid { grid-template-columns: 1fr; } }
</style>
```

- [ ] **Step 2: Commit**

```bash
git add src/components/FeatureGrid.astro
git commit -m "feat: add feature grid section for homepage"
git push
```

---

### Task 9: NewsletterSignup React island

**Files:**
- Create: `src/components/NewsletterSignup.tsx`

- [ ] **Step 1: Write the component**

Create `src/components/NewsletterSignup.tsx`:

```tsx
import { useState } from 'react';

type Status = 'idle' | 'submitting' | 'success' | 'error';

export default function NewsletterSignup({ inline = false }: { inline?: boolean }) {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState<Status>('idle');
  const [msg, setMsg] = useState('');

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setStatus('submitting');
    setMsg('');
    try {
      const res = await fetch('/api/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.error || 'Something went wrong');
      }
      setStatus('success');
      setMsg("You're in. Watch your inbox.");
      setEmail('');
    } catch (err: any) {
      setStatus('error');
      setMsg(err.message || 'Something went wrong');
    }
  }

  return (
    <form onSubmit={submit} className={inline ? 'newsletter newsletter-inline' : 'newsletter'}>
      <input
        type="email"
        required
        placeholder="your@email.com"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        disabled={status === 'submitting'}
        aria-label="Email address"
      />
      <button type="submit" disabled={status === 'submitting' || !email}>
        {status === 'submitting' ? 'Subscribing…' : 'Subscribe'}
      </button>
      {status === 'success' && <div className="msg ok">{msg}</div>}
      {status === 'error' && <div className="msg err">{msg}</div>}
      <style>{`
        .newsletter { display: flex; flex-direction: column; gap: 8px; max-width: 360px; }
        .newsletter-inline { flex-direction: row; align-items: center; max-width: 460px; }
        .newsletter input {
          background: var(--color-bg-elevated);
          border: 1px solid var(--color-border-strong);
          border-radius: 4px;
          padding: 10px 14px;
          color: var(--color-text-primary);
          font-size: 13px;
          font-family: var(--font-sans);
          flex: 1;
        }
        .newsletter input:focus { outline: none; border-color: var(--color-accent-blue); }
        .newsletter button {
          background: var(--color-text-primary);
          color: var(--color-bg);
          border: none;
          border-radius: 4px;
          padding: 10px 18px;
          font-size: 13px;
          font-weight: 600;
          cursor: pointer;
        }
        .newsletter button:disabled { opacity: 0.6; cursor: not-allowed; }
        .msg { font-size: 12px; font-family: var(--font-mono); }
        .msg.ok { color: var(--color-success); }
        .msg.err { color: #ff7a9a; }
      `}</style>
    </form>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add src/components/NewsletterSignup.tsx
git commit -m "feat: add NewsletterSignup React island posting to /api/subscribe"
git push
```

---

### Task 10: Vercel serverless endpoint for newsletter

**Files:**
- Create: `api/subscribe.ts` (Vercel serverless function)
- Create: `.env.example`

- [ ] **Step 1: Install Vercel types**

```bash
npm install -D @vercel/node
```

- [ ] **Step 2: Write the endpoint**

Create `api/subscribe.ts`:

```ts
import type { VercelRequest, VercelResponse } from '@vercel/node';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  const { email } = (req.body || {}) as { email?: string };
  if (!email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    return res.status(400).json({ error: 'Valid email required' });
  }
  const apiKey = process.env.BUTTONDOWN_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: 'Newsletter not configured' });
  }
  try {
    const resp = await fetch('https://api.buttondown.email/v1/subscribers', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email_address: email, type: 'regular' }),
    });
    if (!resp.ok && resp.status !== 400) {
      return res.status(502).json({ error: 'Upstream error' });
    }
    return res.status(200).json({ ok: true });
  } catch (err) {
    return res.status(500).json({ error: 'Network error' });
  }
}
```

- [ ] **Step 3: Write .env.example**

Create `.env.example`:

```
# Buttondown — https://buttondown.email/settings/programming
BUTTONDOWN_API_KEY=

# Formspree — https://formspree.io/
FORMSPREE_FORM_ID=

# Plausible (optional — falls back to no analytics if empty)
PUBLIC_PLAUSIBLE_DOMAIN=orbitalml.com
```

Add `.env` to `.gitignore` (ensure it's present — should already be from Astro scaffold):

```bash
grep -q '^\.env$' .gitignore || echo '.env' >> .gitignore
```

- [ ] **Step 4: Commit**

```bash
git add api/subscribe.ts .env.example .gitignore package.json package-lock.json
git commit -m "feat: add /api/subscribe Vercel endpoint posting to Buttondown"
git push
```

---

### Task 11: Homepage wiring

**Files:**
- Modify: `src/pages/index.astro` (delete Astro-scaffolded default, replace)

- [ ] **Step 1: Write the homepage**

Overwrite `src/pages/index.astro`:

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import Hero from '../components/Hero.astro';
import FeatureGrid from '../components/FeatureGrid.astro';
import NewsletterSignup from '../components/NewsletterSignup.tsx';
---

<BaseLayout title="orbitalml">
  <Hero />
  <FeatureGrid />
  <section class="newsletter-section">
    <div class="container newsletter-block">
      <div>
        <div class="micro-label">STAY IN THE LOOP</div>
        <h2>Monthly: benchmarks, case studies, and new tutorials.</h2>
        <p>No spam. Unsubscribe any time.</p>
      </div>
      <NewsletterSignup client:visible inline={true} />
    </div>
  </section>
</BaseLayout>

<style>
  .newsletter-section {
    padding: var(--space-16) 0;
    border-top: 1px solid var(--color-border);
  }
  .newsletter-block {
    display: grid;
    grid-template-columns: 1.2fr 1fr;
    gap: var(--space-8);
    align-items: center;
  }
  @media (max-width: 1024px) {
    .newsletter-block { grid-template-columns: 1fr; }
  }
</style>
```

- [ ] **Step 2: Run dev server and visually verify**

```bash
npm run dev
```

Open `http://localhost:4321`. Verify:
- Hero displays with gradient headline, constellation viz animates, tooltips show.
- Feature grid renders with 4 cards.
- Newsletter block appears at bottom.
- Nav and footer are present.

Stop server (Ctrl+C).

- [ ] **Step 3: Run build**

```bash
npm run build
```

Expected: 0 errors, `dist/index.html` produced.

- [ ] **Step 4: Commit**

```bash
git add src/pages/index.astro
git commit -m "feat: wire up homepage with hero, features, and newsletter"
git push
```

---

## Phase 3: Learn Section (Pyodide Tutorials)

### Task 12: CodeRunner React island with Pyodide

**Files:**
- Create: `src/components/CodeRunner.tsx`

- [ ] **Step 1: Write the CodeRunner**

Create `src/components/CodeRunner.tsx`:

```tsx
import { useEffect, useRef, useState } from 'react';

// Pyodide types are loose; using `any` on the dynamic import is fine.
declare global {
  interface Window { loadPyodide?: (opts?: any) => Promise<any>; }
}

const PYODIDE_VERSION = '0.26.2';
const PYODIDE_CDN = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full`;

// Module-level singleton so multiple CodeRunner instances share one Pyodide.
let pyodidePromise: Promise<any> | null = null;

function loadPyodideOnce(): Promise<any> {
  if (pyodidePromise) return pyodidePromise;
  pyodidePromise = (async () => {
    if (!window.loadPyodide) {
      await new Promise<void>((resolve, reject) => {
        const s = document.createElement('script');
        s.src = `${PYODIDE_CDN}/pyodide.js`;
        s.onload = () => resolve();
        s.onerror = () => reject(new Error('Failed to load Pyodide'));
        document.head.appendChild(s);
      });
    }
    const pyodide = await window.loadPyodide!({ indexURL: `${PYODIDE_CDN}/` });
    await pyodide.loadPackage(['micropip']);
    const micropip = pyodide.pyimport('micropip');
    // Pure-Python dependency of orbit4ml.sim
    await micropip.install(['sgp4']);
    // orbit4ml itself — install from the same project to pick up the latest
    // released version on PyPI.
    await micropip.install(['orbit4ml']);
    return pyodide;
  })();
  return pyodidePromise;
}

export default function CodeRunner({
  initial,
  height = 180,
}: {
  initial: string;
  height?: number;
}) {
  const [code, setCode] = useState(initial);
  const [output, setOutput] = useState<string>('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'running' | 'error'>('idle');
  const [pyReady, setPyReady] = useState(false);
  const taRef = useRef<HTMLTextAreaElement>(null);

  async function run() {
    setStatus(pyReady ? 'running' : 'loading');
    setOutput('');
    try {
      const pyodide = await loadPyodideOnce();
      setPyReady(true);
      // Capture stdout
      pyodide.runPython(`
import sys, io
_stdout = io.StringIO()
sys.stdout = _stdout
      `);
      try {
        await pyodide.runPythonAsync(code);
      } finally {
        pyodide.runPython(`sys.stdout = sys.__stdout__`);
      }
      const captured = pyodide.runPython(`_stdout.getvalue()`) as string;
      setOutput(captured || '(no output)');
      setStatus('idle');
    } catch (err: any) {
      setOutput(String(err?.message || err));
      setStatus('error');
    }
  }

  function reset() {
    setCode(initial);
    setOutput('');
    setStatus('idle');
  }

  return (
    <div className="code-runner">
      <div className="toolbar">
        <span className="tag">python</span>
        <div className="spacer" />
        <button onClick={reset} className="btn-ghost">Reset</button>
        <button onClick={run} disabled={status === 'loading' || status === 'running'} className="btn-run">
          {status === 'loading' ? 'Loading Pyodide…' : status === 'running' ? 'Running…' : 'Run ▶'}
        </button>
      </div>
      <textarea
        ref={taRef}
        value={code}
        onChange={(e) => setCode(e.target.value)}
        spellCheck={false}
        style={{ height: `${height}px` }}
      />
      {output && (
        <pre className={status === 'error' ? 'output error' : 'output'}>{output}</pre>
      )}
      <style>{`
        .code-runner {
          border: 1px solid var(--color-border);
          border-radius: var(--radius-md);
          background: var(--color-bg-elevated);
          margin: 16px 0;
          overflow: hidden;
        }
        .toolbar {
          display: flex;
          align-items: center;
          padding: 8px 12px;
          border-bottom: 1px solid var(--color-border);
          font-size: 11px;
          gap: 8px;
        }
        .tag {
          font-family: var(--font-mono);
          color: var(--color-text-muted);
          letter-spacing: 1px;
          text-transform: uppercase;
        }
        .spacer { flex: 1; }
        button {
          border: 1px solid var(--color-border-strong);
          background: transparent;
          color: var(--color-text-primary);
          font-size: 11px;
          padding: 4px 12px;
          border-radius: 3px;
          cursor: pointer;
          font-family: var(--font-sans);
        }
        .btn-run {
          background: var(--color-accent-blue);
          color: var(--color-bg);
          border-color: var(--color-accent-blue);
          font-weight: 600;
        }
        .btn-run:disabled { opacity: 0.6; cursor: wait; }
        textarea {
          width: 100%;
          border: none;
          background: transparent;
          color: var(--color-text-primary);
          font-family: var(--font-mono);
          font-size: 13px;
          padding: 14px;
          resize: vertical;
          outline: none;
        }
        .output {
          margin: 0;
          padding: 14px;
          border-top: 1px solid var(--color-border);
          background: #07090f;
          font-family: var(--font-mono);
          font-size: 12px;
          color: var(--color-text-secondary);
          white-space: pre-wrap;
          max-height: 240px;
          overflow: auto;
        }
        .output.error { color: #ff7a9a; }
      `}</style>
    </div>
  );
}
```

- [ ] **Step 2: Verify it type-checks**

```bash
npx astro check
```

Expected: 0 errors.

- [ ] **Step 3: Commit**

```bash
git add src/components/CodeRunner.tsx
git commit -m "feat: add Pyodide-backed CodeRunner React island"
git push
```

---

### Task 13: Content collections setup for tutorials and blog

**Files:**
- Create: `src/content/config.ts`, `src/content/tutorials/.gitkeep`, `src/content/blog/.gitkeep`

- [ ] **Step 1: Define collections**

Create `src/content/config.ts`:

```ts
import { defineCollection, z } from 'astro:content';

const tutorials = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    order: z.number(),
    level: z.enum(['beginner', 'intermediate', 'advanced']),
    duration_minutes: z.number(),
    updated: z.date(),
  }),
});

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.date(),
    author: z.string().default('Mainak Mallick'),
    tags: z.array(z.string()).default([]),
  }),
});

export const collections = { tutorials, blog };
```

- [ ] **Step 2: Create directories**

```bash
mkdir -p src/content/tutorials src/content/blog
touch src/content/tutorials/.gitkeep src/content/blog/.gitkeep
```

- [ ] **Step 3: Commit**

```bash
git add src/content/
git commit -m "feat: define content collections for tutorials and blog"
git push
```

---

### Task 14: Tutorial layout

**Files:**
- Create: `src/layouts/TutorialLayout.astro`

- [ ] **Step 1: Write the layout**

Create `src/layouts/TutorialLayout.astro`:

```astro
---
import BaseLayout from './BaseLayout.astro';
import type { CollectionEntry } from 'astro:content';

export interface Props {
  entry: CollectionEntry<'tutorials'>;
}

const { entry } = Astro.props;
const { title, description, level, duration_minutes, updated } = entry.data;
const levelLabel = level.charAt(0).toUpperCase() + level.slice(1);
---

<BaseLayout title={title} description={description}>
  <article class="tutorial">
    <div class="container">
      <header class="tut-head">
        <a href="/learn" class="back">← Learn</a>
        <div class="meta">
          <span class="tag">{levelLabel}</span>
          <span class="tag">{duration_minutes} min</span>
          <span class="tag">Updated {updated.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}</span>
        </div>
        <h1>{title}</h1>
        <p class="desc">{description}</p>
      </header>
      <div class="prose">
        <slot />
      </div>
      <footer class="tut-foot">
        <a href="/learn" class="back">← All tutorials</a>
      </footer>
    </div>
  </article>
</BaseLayout>

<style is:global>
  .tutorial .prose {
    max-width: 720px;
    margin: 0 auto;
    padding: var(--space-8) 0 var(--space-12);
  }
  .tutorial .prose h2 { margin-top: var(--space-10); }
  .tutorial .prose h3 { margin-top: var(--space-8); }
  .tutorial .prose p { font-size: 15px; line-height: 1.65; }
  .tutorial .prose a { color: var(--color-accent-blue); border-bottom: 1px solid transparent; }
  .tutorial .prose a:hover { border-bottom-color: var(--color-accent-blue); }
  .tutorial .prose ul, .tutorial .prose ol { padding-left: 1.4em; color: var(--color-text-secondary); }
  .tutorial .prose li { margin-bottom: 6px; }
</style>

<style>
  .tut-head { max-width: 720px; margin: var(--space-10) auto 0; }
  .back { font-family: var(--font-mono); font-size: 12px; color: var(--color-text-muted); display: inline-block; margin-bottom: var(--space-4); }
  .back:hover { color: var(--color-accent-blue); }
  .meta { display: flex; gap: 10px; margin-bottom: var(--space-4); }
  .tag {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 3px 8px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    color: var(--color-text-muted);
  }
  .desc { font-size: 16px; color: var(--color-text-secondary); max-width: 600px; margin-top: var(--space-3); }
  .tut-foot { max-width: 720px; margin: 0 auto; padding: var(--space-8) 0; border-top: 1px solid var(--color-border); }
</style>
```

- [ ] **Step 2: Commit**

```bash
git add src/layouts/TutorialLayout.astro
git commit -m "feat: add tutorial layout with meta bar and prose styling"
git push
```

---

### Task 15: Dynamic tutorial route

**Files:**
- Create: `src/pages/learn/[...slug].astro`

- [ ] **Step 1: Write the dynamic route**

Create `src/pages/learn/[...slug].astro`:

```astro
---
import { getCollection, type CollectionEntry } from 'astro:content';
import TutorialLayout from '../../layouts/TutorialLayout.astro';

export async function getStaticPaths() {
  const entries = await getCollection('tutorials');
  return entries.map((entry) => ({
    params: { slug: entry.slug },
    props: { entry },
  }));
}

interface Props { entry: CollectionEntry<'tutorials'>; }
const { entry } = Astro.props;
const { Content } = await entry.render();
---

<TutorialLayout entry={entry}>
  <Content />
</TutorialLayout>
```

- [ ] **Step 2: Commit**

```bash
git add src/pages/learn/
git commit -m "feat: add dynamic tutorial route rendering MDX with TutorialLayout"
git push
```

---

### Task 16: Tutorial 1 — Getting Started

**Files:**
- Create: `src/content/tutorials/getting-started.mdx`

- [ ] **Step 1: Write the tutorial**

Create `src/content/tutorials/getting-started.mdx`:

```mdx
---
title: Getting Started
description: Your first orbit4ml simulation — define a constellation and watch satellites orbit, all in the browser.
order: 1
level: beginner
duration_minutes: 5
updated: 2026-04-19
---

import CodeRunner from '../../components/CodeRunner.tsx';

Welcome. In 5 minutes you'll define a satellite constellation and see it orbit — without installing anything.

## What orbit4ml does

`orbit4ml` is an open-source Python library for machine learning in space. Its core module, `orbit4ml.sim`, gives you a physics-based **digital twin** of a satellite constellation: real orbital mechanics (SGP4), eclipse cycles, thermal budgets, inter-satellite links, and hardware fault injection.

You use it to answer questions like: *how much of the time could I actually train a model on this constellation?*

## Your first constellation

The constellation below is a Walker-delta pattern — 6 planes of 11 satellites each, at 550 km altitude. That's the size and shape of a Starlink-ish LEO constellation.

Click **Run ▶** to execute it in your browser.

<CodeRunner client:visible initial={`from orbit4ml.sim import Constellation

constellation = Constellation(
    planes=6,
    sats_per_plane=11,
    altitude=550,
    inclination=53.0,
)

print(f"Total satellites: {constellation.total_satellites}")
print(f"First 3 IDs: {constellation.satellite_ids[:3]}")
print(f"Semi-major axis: {constellation.semi_major_axis:.1f} km")
`} />

The first run takes ~8 seconds — Python is loading in your browser. After that, every run is instant.

## Next

- **[Simulating a Constellation →](/learn/simulating-a-constellation)** — step through time and watch satellites cycle through eclipse.
- **[Training Under Eclipse →](/learn/training-under-eclipse)** — gate a PyTorch training loop on real orbital constraints.

Prefer to work locally? The library ships on PyPI:

```bash
pip install orbit4ml
```

All code from these tutorials works identically on your machine.
```

- [ ] **Step 2: Commit**

```bash
git add src/content/tutorials/getting-started.mdx
git commit -m "feat: add Getting Started tutorial with runnable first example"
git push
```

---

### Task 17: Tutorial 2 — Simulating a Constellation

**Files:**
- Create: `src/content/tutorials/simulating-a-constellation.mdx`

- [ ] **Step 1: Write the tutorial**

Create `src/content/tutorials/simulating-a-constellation.mdx`:

```mdx
---
title: Simulating a Constellation
description: Propagate a satellite constellation through an hour of orbit and see who is sunlit vs eclipsed at each minute.
order: 2
level: beginner
duration_minutes: 8
updated: 2026-04-19
---

import CodeRunner from '../../components/CodeRunner.tsx';

You've defined a constellation. Now let's watch it evolve.

## The digital twin

`DigitalTwin` wraps a `Constellation` with physics models: SGP4 orbit propagation, an eclipse model, thermal budgets, inter-satellite links, and fault injection. Calling `propagate()` gives you an iterator over **`EpochState`** snapshots — one per time step.

Each `EpochState.satellites` is a list of per-satellite state objects with `.power`, `.thermal`, `.links`, and `.faults` attributes.

## Watch satellites enter eclipse

Run this to propagate a 66-satellite constellation for one hour of simulated time. The output shows how many satellites are sunlit vs in Earth's shadow at each minute.

<CodeRunner
  client:visible
  height={260}
  initial={`from datetime import datetime
from orbit4ml.sim import Constellation, DigitalTwin

constellation = Constellation(
    planes=6, sats_per_plane=11, altitude=550, inclination=53.0
)
twin = DigitalTwin(constellation)

start = datetime(2026, 6, 1, 12, 0, 0)
print(f"{'Time':<10}{'Sunlit':>8}{'Eclipse':>10}")
print("-" * 30)

for epoch in twin.propagate(start=start, hours=1.0, step_seconds=300):
    sunlit = sum(1 for s in epoch.satellites if s.power.available)
    eclipse = len(epoch.satellites) - sunlit
    ts = epoch.timestamp.strftime("%H:%M")
    print(f"{ts:<10}{sunlit:>8}{eclipse:>10}")
`} />

## What you're seeing

At any moment, roughly one-third of a LEO constellation is in eclipse — Earth is blocking the Sun from that satellite's perspective. In a 92-minute orbit, each satellite spends ~35 minutes in shadow.

That shadow matters: no sunlight means no solar power means **no training**. This is the constraint `orbit4ml` makes visible.

## Per-satellite detail

Want to see a single satellite's state at a specific time?

<CodeRunner
  client:visible
  height={240}
  initial={`from datetime import datetime
from orbit4ml.sim import Constellation, DigitalTwin

constellation = Constellation(planes=6, sats_per_plane=11, altitude=550, inclination=53.0)
twin = DigitalTwin(constellation)

for epoch in twin.propagate(start=datetime(2026, 6, 1, 12, 0, 0), hours=0.1, step_seconds=60):
    sat = epoch.satellites[0]
    print(f"[{epoch.timestamp.strftime('%H:%M:%S')}] {sat.id}")
    print(f"  power.available: {sat.power.available}")
    print(f"  power.watts:     {sat.power.watts:.1f}")
    print(f"  thermal.within_budget: {sat.thermal.within_budget}")
    print(f"  thermal.gpu_budget_watts: {sat.thermal.gpu_budget_watts:.1f}")
    print("---")
`} />

## Next

You now have a propagating digital twin. The missing piece: gating actual ML training on these constraints.

**[Training Under Eclipse →](/learn/training-under-eclipse)**
```

- [ ] **Step 2: Commit**

```bash
git add src/content/tutorials/simulating-a-constellation.mdx
git commit -m "feat: add Simulating a Constellation tutorial"
git push
```

---

### Task 18: Tutorial 3 — Training Under Eclipse

**Files:**
- Create: `src/content/tutorials/training-under-eclipse.mdx`

- [ ] **Step 1: Write the tutorial**

Create `src/content/tutorials/training-under-eclipse.mdx`:

```mdx
---
title: Training Under Eclipse
description: Gate a minimal Python training loop on power and thermal state. See the 70% utilization ceiling emerge from physics.
order: 3
level: intermediate
duration_minutes: 10
updated: 2026-04-19
---

import CodeRunner from '../../components/CodeRunner.tsx';

Here's the punchline of space ML: **you can only train when your satellite has power and thermal headroom**. Everything else is downstream of that.

This tutorial uses pure-Python tensor math (no PyTorch) so it runs in your browser. The pattern is identical when you swap in real frameworks.

## The training-gate pattern

```python
for epoch in twin.propagate(...):
    for sat in epoch.satellites:
        if sat.power.available and sat.thermal.within_budget:
            # TRAIN
            ...
        else:
            # IDLE (or checkpoint, or queue gradients for later)
            ...
```

Two booleans. That's the whole interface `orbit4ml.sim` exposes to a training loop.

## Measure your training utilization

This snippet counts satellite-minutes that were trainable vs idle across a 30-minute window.

<CodeRunner
  client:visible
  height={300}
  initial={`from datetime import datetime
from orbit4ml.sim import Constellation, DigitalTwin

constellation = Constellation(
    planes=6, sats_per_plane=11, altitude=550, inclination=53.0
)
twin = DigitalTwin(constellation)

train_steps = 0
idle_steps = 0
total_steps = 0
fault_events = 0

for epoch in twin.propagate(start=datetime(2026, 6, 1, 12, 0, 0), hours=0.5, step_seconds=60):
    for sat in epoch.satellites:
        total_steps += 1
        if sat.faults.active:
            fault_events += 1
        if sat.power.available and sat.thermal.within_budget and not sat.faults.active:
            train_steps += 1
        else:
            idle_steps += 1

print(f"Total satellite-minutes: {total_steps}")
print(f"  Trained:      {train_steps:>5} ({train_steps/total_steps*100:.1f}%)")
print(f"  Idle:         {idle_steps:>5} ({idle_steps/total_steps*100:.1f}%)")
print(f"  Fault events: {fault_events}")
`} />

Expect ~70% training utilization. The rest is shadow, thermal throttle, and stochastic faults. That ceiling is not a bug — it's physics.

## Going further

- Swap in a real model (`torch.nn`) and gate `loss.backward()` the same way — works identically
- Use `sat.thermal.gpu_budget_watts` to dynamically resize your batch, not just skip
- Hand off incomplete gradients to peers via `sat.links` (coming in `orbit4ml.fed` v1.0)

For heavier experiments with real PyTorch models, try the [Playground](/playground) (JupyterLite with GPU-capable builds) or [open the full MVP script in Colab](https://colab.research.google.com/github/orbit-ml/orbit4ml/blob/main/examples/mvp_training_loop.py).

## You're caught up

You've now:

1. Defined a constellation
2. Propagated a digital twin through time
3. Gated training on real orbital constraints

Next stop: the [Playground](/playground) for free-form exploration, or [Benchmarks](/benchmarks) for reference numbers.
```

- [ ] **Step 2: Commit**

```bash
git add src/content/tutorials/training-under-eclipse.mdx
git commit -m "feat: add Training Under Eclipse tutorial"
git push
```

---

### Task 19: Learn index page

**Files:**
- Create: `src/pages/learn/index.astro`

- [ ] **Step 1: Write the index**

Create `src/pages/learn/index.astro`:

```astro
---
import BaseLayout from '../../layouts/BaseLayout.astro';
import { getCollection } from 'astro:content';

const tutorials = (await getCollection('tutorials')).sort((a, b) => a.data.order - b.data.order);
---

<BaseLayout title="Learn" description="Interactive, in-browser tutorials for orbit4ml. No install required.">
  <section class="learn">
    <div class="container">
      <div class="head">
        <div class="micro-label">LEARN</div>
        <h1>Interactive tutorials.<br/>No install, no signup.</h1>
        <p class="sub">Every code block on every page runs in your browser. Edit, hit Run, see output.</p>
      </div>
      <ol class="list">
        {tutorials.map((t) => (
          <li>
            <a href={`/learn/${t.slug}`}>
              <div class="num">{String(t.data.order).padStart(2, '0')}</div>
              <div class="body">
                <div class="meta">
                  <span class="tag">{t.data.level}</span>
                  <span class="tag">{t.data.duration_minutes} min</span>
                </div>
                <h3>{t.data.title}</h3>
                <p>{t.data.description}</p>
                <span class="cta">Start tutorial →</span>
              </div>
            </a>
          </li>
        ))}
      </ol>
    </div>
  </section>
</BaseLayout>

<style>
  .learn { padding: var(--space-12) 0 var(--space-16); }
  .head { max-width: 720px; margin-bottom: var(--space-12); }
  .sub { font-size: 16px; max-width: 540px; margin-top: var(--space-3); }
  .list { list-style: none; padding: 0; margin: 0; display: grid; gap: var(--space-4); }
  .list a {
    display: grid;
    grid-template-columns: 60px 1fr;
    gap: var(--space-5);
    padding: var(--space-5);
    background: var(--color-bg-elevated);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    transition: border-color 0.15s, transform 0.15s;
  }
  .list a:hover {
    border-color: var(--color-accent-blue);
    transform: translateY(-2px);
    color: var(--color-text-primary);
  }
  .num {
    font-family: var(--font-mono);
    font-size: 26px;
    color: var(--color-accent-blue);
    font-weight: 500;
  }
  .meta { display: flex; gap: 8px; margin-bottom: var(--space-2); }
  .tag {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 2px 7px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    color: var(--color-text-muted);
  }
  .body h3 { color: var(--color-text-primary); margin: 4px 0 6px; }
  .body p { font-size: 13px; margin-bottom: var(--space-3); }
  .cta { font-family: var(--font-mono); font-size: 11px; color: var(--color-accent-blue); }
</style>
```

- [ ] **Step 2: Run dev and visually confirm**

```bash
npm run dev
```

Visit `http://localhost:4321/learn`. Verify: three tutorials listed in order, links resolve, a tutorial page renders with TutorialLayout and executes a Pyodide code block. Stop the server.

- [ ] **Step 3: Commit**

```bash
git add src/pages/learn/index.astro
git commit -m "feat: add Learn index listing all tutorials"
git push
```

---

## Phase 4: Playground

### Task 20: Playground page (JupyterLite)

**Files:**
- Create: `src/pages/playground.astro`

- [ ] **Step 1: Write the page**

Create `src/pages/playground.astro`:

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
// We embed an upstream JupyterLite deployment. Running a self-hosted JupyterLite
// with orbit4ml pre-installed is a follow-up improvement; for v1 we embed the
// public JupyterLite and rely on a pyodide-based kernel + %pip install.
const JUPYTERLITE_URL = 'https://jupyterlite.readthedocs.io/en/stable/_static/lab/index.html';
---

<BaseLayout
  title="Playground"
  description="Free-form Python notebook in your browser, pre-loaded with orbit4ml."
>
  <section class="playground">
    <div class="container head">
      <div class="micro-label">PLAYGROUND</div>
      <h1>Free-form Python, right here.</h1>
      <p>JupyterLite running entirely in your browser. Start with the snippet below to install orbit4ml.</p>
      <pre><code>{`%pip install orbit4ml
from orbit4ml.sim import Constellation, DigitalTwin`}</code></pre>
    </div>
    <div class="frame-wrap">
      <iframe
        src={JUPYTERLITE_URL}
        title="JupyterLite playground"
        loading="lazy"
        allow="cross-origin-isolated"
      ></iframe>
    </div>
  </section>
</BaseLayout>

<style>
  .playground { padding: var(--space-10) 0 var(--space-16); }
  .head { max-width: 720px; margin-bottom: var(--space-8); }
  .head p { margin-bottom: var(--space-4); }
  .frame-wrap {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 var(--space-6);
  }
  iframe {
    width: 100%;
    height: 720px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    background: var(--color-bg-elevated);
  }
</style>
```

- [ ] **Step 2: Commit**

```bash
git add src/pages/playground.astro
git commit -m "feat: add Playground page embedding JupyterLite"
git push
```

---

## Phase 5: Blog and Remaining Pages

### Task 21: Blog layout and dynamic route

**Files:**
- Create: `src/layouts/BlogLayout.astro`, `src/pages/blog/[...slug].astro`

- [ ] **Step 1: Write BlogLayout**

Create `src/layouts/BlogLayout.astro`:

```astro
---
import BaseLayout from './BaseLayout.astro';
import type { CollectionEntry } from 'astro:content';

export interface Props { entry: CollectionEntry<'blog'>; }
const { entry } = Astro.props;
const { title, description, date, author, tags } = entry.data;
---

<BaseLayout title={title} description={description}>
  <article class="post">
    <div class="container">
      <header class="post-head">
        <a href="/blog" class="back">← Blog</a>
        <div class="meta">
          <span>{author}</span>
          <span>·</span>
          <span>{date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}</span>
        </div>
        <h1>{title}</h1>
        <p class="desc">{description}</p>
        {tags.length > 0 && (
          <div class="tags">{tags.map((t: string) => <span class="tag">{t}</span>)}</div>
        )}
      </header>
      <div class="prose"><slot /></div>
    </div>
  </article>
</BaseLayout>

<style is:global>
  .post .prose {
    max-width: 720px;
    margin: 0 auto;
    padding: var(--space-8) 0 var(--space-12);
  }
  .post .prose h2 { margin-top: var(--space-10); }
  .post .prose p { font-size: 15px; line-height: 1.7; }
  .post .prose a { color: var(--color-accent-blue); border-bottom: 1px solid transparent; }
  .post .prose a:hover { border-bottom-color: var(--color-accent-blue); }
  .post .prose blockquote {
    border-left: 2px solid var(--color-accent-blue);
    margin: var(--space-5) 0;
    padding-left: var(--space-4);
    color: var(--color-text-secondary);
    font-style: italic;
  }
</style>

<style>
  .post-head { max-width: 720px; margin: var(--space-10) auto 0; }
  .back { font-family: var(--font-mono); font-size: 12px; color: var(--color-text-muted); display: inline-block; margin-bottom: var(--space-4); }
  .meta { font-family: var(--font-mono); font-size: 11px; color: var(--color-text-muted); display: flex; gap: 8px; margin-bottom: var(--space-4); }
  .desc { font-size: 16px; color: var(--color-text-secondary); max-width: 600px; margin-top: var(--space-3); }
  .tags { display: flex; gap: 8px; margin-top: var(--space-4); }
  .tag { font-family: var(--font-mono); font-size: 10px; padding: 2px 8px; border: 1px solid var(--color-border); border-radius: var(--radius-sm); color: var(--color-text-muted); }
</style>
```

- [ ] **Step 2: Write dynamic route**

Create `src/pages/blog/[...slug].astro`:

```astro
---
import { getCollection, type CollectionEntry } from 'astro:content';
import BlogLayout from '../../layouts/BlogLayout.astro';

export async function getStaticPaths() {
  const entries = await getCollection('blog');
  return entries.map((entry) => ({
    params: { slug: entry.slug },
    props: { entry },
  }));
}

interface Props { entry: CollectionEntry<'blog'>; }
const { entry } = Astro.props;
const { Content } = await entry.render();
---

<BlogLayout entry={entry}>
  <Content />
</BlogLayout>
```

- [ ] **Step 3: Commit**

```bash
git add src/layouts/BlogLayout.astro src/pages/blog/
git commit -m "feat: add blog layout and dynamic MDX route"
git push
```

---

### Task 22: Blog index page

**Files:**
- Create: `src/pages/blog/index.astro`

- [ ] **Step 1: Write it**

Create `src/pages/blog/index.astro`:

```astro
---
import BaseLayout from '../../layouts/BaseLayout.astro';
import { getCollection } from 'astro:content';

const posts = (await getCollection('blog'))
  .sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
---

<BaseLayout title="Blog" description="Thought leadership, benchmarks, and case studies from the orbitalml team.">
  <section class="blog">
    <div class="container">
      <div class="head">
        <div class="micro-label">BLOG</div>
        <h1>Case studies, benchmarks,<br/>and the road to space ML.</h1>
      </div>
      <ul class="list">
        {posts.map((p) => (
          <li>
            <a href={`/blog/${p.slug}`}>
              <div class="meta">
                <span>{p.data.date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })}</span>
                <span>·</span>
                <span>{p.data.author}</span>
              </div>
              <h2>{p.data.title}</h2>
              <p>{p.data.description}</p>
            </a>
          </li>
        ))}
      </ul>
    </div>
  </section>
</BaseLayout>

<style>
  .blog { padding: var(--space-12) 0 var(--space-16); }
  .head { max-width: 720px; margin-bottom: var(--space-12); }
  .list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: var(--space-5); max-width: 840px; }
  .list a { display: block; padding: var(--space-6); border: 1px solid var(--color-border); border-radius: var(--radius-lg); transition: border-color 0.15s, transform 0.15s; background: var(--color-bg-elevated); }
  .list a:hover { border-color: var(--color-accent-blue); transform: translateY(-2px); color: var(--color-text-primary); }
  .meta { font-family: var(--font-mono); font-size: 11px; color: var(--color-text-muted); display: flex; gap: 6px; margin-bottom: var(--space-2); }
  .list h2 { font-size: 22px; color: var(--color-text-primary); margin-bottom: var(--space-2); }
  .list p { font-size: 14px; color: var(--color-text-secondary); margin: 0; }
</style>
```

- [ ] **Step 2: Commit**

```bash
git add src/pages/blog/index.astro
git commit -m "feat: add blog index with post list"
git push
```

---

### Task 23: Launch blog post — "Introducing orbitalml"

**Files:**
- Create: `src/content/blog/introducing-planet-harness.mdx`

- [ ] **Step 1: Write the post**

Create `src/content/blog/introducing-planet-harness.mdx`:

```mdx
---
title: "Introducing orbitalml"
description: "A new home for open-source machine learning in space — interactive tutorials, real benchmarks, zero install friction."
date: 2026-04-19
author: Mainak Mallick
tags: [announcement, orbit4ml]
---

Today we're launching **orbitalml**: the interactive front door for `orbit4ml`, our open ecosystem for machine learning in space.

Until today, if you wanted to understand what it takes to train ML models in orbit, your choices were: read dense aerospace papers, dig into the `orbit4ml` API docs, or run our library locally. All three are valid. None of them are *exciting*.

orbitalml fixes that.

## What you'll find here

- **Learn** — three interactive tutorials that run Python in your browser. No `pip install`, no signup, no notebook to configure. Click Run, see output.
- **Playground** — a full JupyterLite notebook pre-loaded with `orbit4ml`. Explore freely.
- **Benchmarks** — published numbers on what the library can actually do, updated as the project evolves.
- **For Missions** — if you're building a real space mission and need commercial-grade ML runtime (not just the open library), this is where you get in touch.

## Why this matters

Space ML is hard *because the physics is unforgiving*, not because Python is hard. An L2-bound CubeSat with a 100W solar panel and a 25°C thermal budget is a very different compute environment than a data center. Every shortcut you take on the ground is a mission risk in orbit.

`orbit4ml` makes those constraints first-class in your code: `if sat.power.available and sat.thermal.within_budget: train()` is the whole abstraction. orbitalml lets you *feel* that in a browser tab.

## What's next

v1 ships with three tutorials, a playground, and the first round of benchmarks. Coming up:

- `orbit4ml.train` — constraint-aware training loops that checkpoint and resume across eclipse cycles
- `orbit4ml.fed` — federated learning across a constellation with topology-aware aggregation
- More tutorials, more case studies, more benchmarks

If that sounds interesting, [subscribe to the newsletter](/#newsletter) or [star the repo on GitHub](https://github.com/orbit-ml/orbit4ml). And if you're flying a real mission with ML on board, [come talk to us](/missions).

Welcome to orbitalml. Let's harness the planet.
```

- [ ] **Step 2: Commit**

```bash
git add src/content/blog/introducing-planet-harness.mdx
git commit -m "feat: add launch blog post"
git push
```

---

### Task 24: Case-study blog post — "Why orbital ML bottoms out at 70% utilization"

**Files:**
- Create: `src/content/blog/the-70-percent-ceiling.mdx`

- [ ] **Step 1: Write the post**

Create `src/content/blog/the-70-percent-ceiling.mdx`:

```mdx
---
title: "The 70% ceiling: why orbital ML can't train all the time"
description: "Run our MVP constellation through a digital twin and you'll see training utilization land around 70%. That's not a bug — it's physics."
date: 2026-04-19
author: Mainak Mallick
tags: [benchmark, analysis]
---

If you run the `orbit4ml` MVP script today on a Starlink-ish constellation (66 sats, 550 km altitude, 53° inclination), you'll get this:

```
Training steps (sunlit + thermal OK):  1442
Idle steps (eclipse or thermal limit):  604
Training utilization:                   70.5%
```

Every time. Seed doesn't matter much. Simulation window doesn't change it qualitatively. **Why does it land right around 70%?**

## The physics

A satellite in low Earth orbit spends roughly one-third of every orbit in Earth's shadow. That's geometry — the Earth's diameter divided by the circumference of the orbital path. For a 550 km altitude orbit, that's about 35 minutes of eclipse per 92-minute orbit, or **~62% sunlit**.

Plus thermal slack. Our simplified thermal model gives satellites a bit more budget during eclipse (better radiator efficiency when they're not baking) but less training headroom because the GPUs are already thermally loaded from the prior sunlit period. Net: a few extra minutes of training on the shoulders of each eclipse.

The 62% → 70% gap is the thermal model earning back some of what geometry takes away.

## Why this is load-bearing

If your training loop assumes it can run continuously, you're implicitly assuming either:

1. A dedicated ground station (not realistic for most LEO missions — you see it for ~10 minutes per pass)
2. Infinite battery (radiation-hardened batteries have real capacity limits, and using them for training eats into mission-critical budgets)
3. You'll "catch up" in the sunlit window (which means overshooting your thermal budget)

The 70% ceiling is what's *actually possible* with a realistic power-thermal-geometry stack. Getting higher means relaxing a real constraint — and knowing which constraint you're relaxing is what `orbit4ml.sim` gives you.

## What to do with this number

A few practical implications:

- **Design your learning rate schedule assuming you lose 30% of your compute.** An epoch isn't wall-clock; it's sunlit-minutes.
- **Checkpoint aggressively at eclipse entry.** You're going to cold-start a lot. Save state before you sleep.
- **Batch size should flex with thermal budget**, not stay fixed. `sat.thermal.gpu_budget_watts` is your friend.
- **When you need >70%, switch strategies.** Federated-aggregate across satellites in different orbital planes (they eclipse at different times); each sat contributes whenever it's sunlit.

The next post will get into the third bullet in detail — dynamic batch sizing as a function of thermal budget.

Meanwhile, see it for yourself: **[run the simulation in your browser](/learn/training-under-eclipse)**.
```

- [ ] **Step 2: Commit**

```bash
git add src/content/blog/the-70-percent-ceiling.mdx
git commit -m "feat: add 70% ceiling case-study blog post"
git push
```

---

### Task 25: Benchmarks page

**Files:**
- Create: `src/pages/benchmarks.astro`

- [ ] **Step 1: Write the page**

Create `src/pages/benchmarks.astro`:

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';

const benchmarks = [
  {
    metric: 'Training utilization',
    value: '70.4%',
    subtext: '66-sat LEO constellation, 30-minute window',
    context: 'Fraction of satellite-minutes where power + thermal allowed training. Stable across seeds.',
    source: '/blog/the-70-percent-ceiling',
  },
  {
    metric: 'Average eclipse duration',
    value: '34.8 min',
    subtext: 'per 92-minute orbit at 550 km',
    context: 'Cylindrical shadow model, matches analytical geometry within ±2%.',
    source: null,
  },
  {
    metric: 'Simulation throughput',
    value: '1.1M',
    subtext: 'satellite-steps / sec on a laptop CPU',
    context: 'MVP release. Pre-propagation dominates; single-threaded NumPy.',
    source: null,
  },
  {
    metric: 'Peak ISL active links',
    value: '4.3 avg',
    subtext: 'simultaneous links per satellite',
    context: 'Distance-threshold + line-of-sight model, 5000 km max link.',
    source: null,
  },
];

const upcoming = [
  'orbit4ml.train v0.2 — checkpoint/resume latency across eclipse cycles',
  'orbit4ml.fed v1.0 — gradient aggregation bandwidth under ISL constraints',
  'orbit4ml.compress v0.3 — post-quantization model size vs accuracy on EuroSAT',
];
---

<BaseLayout title="Benchmarks" description="Published performance numbers for orbit4ml. Curated, reproducible, annotated.">
  <section class="bench">
    <div class="container">
      <div class="head">
        <div class="micro-label">BENCHMARKS</div>
        <h1>Published numbers.<br/>No hand-waving.</h1>
        <p class="sub">All benchmarks below are reproducible from the <a href="https://github.com/orbit-ml/orbit4ml">orbit4ml</a> source. We publish the script, the seed, and the environment alongside every number.</p>
      </div>

      <div class="grid">
        {benchmarks.map((b) => (
          <div class="card">
            <div class="metric">{b.metric}</div>
            <div class="value">{b.value}</div>
            <div class="subtext">{b.subtext}</div>
            <p class="context">{b.context}</p>
            {b.source && <a href={b.source} class="source">Read the analysis →</a>}
          </div>
        ))}
      </div>

      <div class="upcoming">
        <div class="micro-label">COMING SOON</div>
        <ul>{upcoming.map((u) => <li>{u}</li>)}</ul>
      </div>
    </div>
  </section>
</BaseLayout>

<style>
  .bench { padding: var(--space-12) 0 var(--space-16); }
  .head { max-width: 720px; margin-bottom: var(--space-12); }
  .sub { font-size: 15px; max-width: 600px; }
  .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: var(--space-5); margin-bottom: var(--space-16); }
  .card { padding: var(--space-6); background: var(--color-bg-elevated); border: 1px solid var(--color-border); border-radius: var(--radius-lg); }
  .metric { font-family: var(--font-mono); font-size: 11px; text-transform: uppercase; letter-spacing: 2px; color: var(--color-text-muted); margin-bottom: var(--space-3); }
  .value { font-size: 40px; font-weight: 600; letter-spacing: -1px; background: var(--color-accent-gradient); -webkit-background-clip: text; background-clip: text; color: transparent; line-height: 1; margin-bottom: var(--space-2); }
  .subtext { font-family: var(--font-mono); font-size: 11px; color: var(--color-text-muted); margin-bottom: var(--space-4); }
  .context { font-size: 13px; margin-bottom: var(--space-3); }
  .source { font-family: var(--font-mono); font-size: 11px; color: var(--color-accent-blue); }
  .upcoming { padding: var(--space-6); border: 1px dashed var(--color-border-strong); border-radius: var(--radius-lg); }
  .upcoming ul { list-style: none; padding: 0; margin: var(--space-4) 0 0; }
  .upcoming li { font-size: 13px; padding: 8px 0; border-bottom: 1px solid var(--color-border); color: var(--color-text-secondary); }
  .upcoming li:last-child { border-bottom: none; }
  @media (max-width: 640px) { .grid { grid-template-columns: 1fr; } }
</style>
```

- [ ] **Step 2: Commit**

```bash
git add src/pages/benchmarks.astro
git commit -m "feat: add benchmarks page with metrics grid and roadmap"
git push
```

---

### Task 26: For Missions page and contact endpoint

**Files:**
- Create: `src/pages/missions.astro`, `api/contact.ts`

- [ ] **Step 1: Write the contact endpoint**

Create `api/contact.ts`:

```ts
import type { VercelRequest, VercelResponse } from '@vercel/node';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  const { name, email, organization, message } = (req.body || {}) as {
    name?: string; email?: string; organization?: string; message?: string;
  };
  if (!name || !email || !message) {
    return res.status(400).json({ error: 'name, email, and message are required' });
  }
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    return res.status(400).json({ error: 'Invalid email' });
  }
  const formId = process.env.FORMSPREE_FORM_ID;
  if (!formId) {
    return res.status(500).json({ error: 'Contact not configured' });
  }
  try {
    const resp = await fetch(`https://formspree.io/f/${formId}`, {
      method: 'POST',
      headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, organization, message, _subject: 'orbitalml — Missions inquiry' }),
    });
    if (!resp.ok) return res.status(502).json({ error: 'Upstream error' });
    return res.status(200).json({ ok: true });
  } catch {
    return res.status(500).json({ error: 'Network error' });
  }
}
```

- [ ] **Step 2: Create MissionsForm React island**

Create `src/components/MissionsForm.tsx`:

```tsx
import { useState } from 'react';

type Status = 'idle' | 'submitting' | 'success' | 'error';

export default function MissionsForm() {
  const [form, setForm] = useState({ name: '', email: '', organization: '', message: '' });
  const [status, setStatus] = useState<Status>('idle');
  const [msg, setMsg] = useState('');

  function update<K extends keyof typeof form>(k: K, v: string) {
    setForm((f) => ({ ...f, [k]: v }));
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setStatus('submitting');
    setMsg('');
    try {
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.error || 'Something went wrong');
      }
      setStatus('success');
      setMsg("Got it. We'll be in touch within a week.");
      setForm({ name: '', email: '', organization: '', message: '' });
    } catch (err: any) {
      setStatus('error');
      setMsg(err.message || 'Something went wrong');
    }
  }

  return (
    <form onSubmit={submit} className="missions-form">
      <div className="row">
        <label>
          <span>Name</span>
          <input required value={form.name} onChange={(e) => update('name', e.target.value)} />
        </label>
        <label>
          <span>Email</span>
          <input required type="email" value={form.email} onChange={(e) => update('email', e.target.value)} />
        </label>
      </div>
      <label>
        <span>Organization (optional)</span>
        <input value={form.organization} onChange={(e) => update('organization', e.target.value)} />
      </label>
      <label>
        <span>Tell us about the mission</span>
        <textarea required rows={5} value={form.message} onChange={(e) => update('message', e.target.value)} />
      </label>
      <button type="submit" disabled={status === 'submitting'}>
        {status === 'submitting' ? 'Sending…' : 'Send'}
      </button>
      {msg && <div className={status === 'error' ? 'msg err' : 'msg ok'}>{msg}</div>}
      <style>{`
        .missions-form { display: flex; flex-direction: column; gap: 14px; max-width: 560px; }
        .row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
        @media (max-width: 640px) { .row { grid-template-columns: 1fr; } }
        label { display: flex; flex-direction: column; gap: 6px; }
        label span { font-family: var(--font-mono); font-size: 10px; letter-spacing: 1px; text-transform: uppercase; color: var(--color-text-muted); }
        input, textarea {
          background: var(--color-bg-elevated);
          border: 1px solid var(--color-border-strong);
          border-radius: 4px;
          padding: 10px 14px;
          color: var(--color-text-primary);
          font-size: 14px;
          font-family: var(--font-sans);
          resize: vertical;
        }
        input:focus, textarea:focus { outline: none; border-color: var(--color-accent-blue); }
        button {
          align-self: flex-start;
          background: var(--color-text-primary);
          color: var(--color-bg);
          border: none;
          border-radius: 4px;
          padding: 10px 20px;
          font-size: 13px;
          font-weight: 600;
          cursor: pointer;
        }
        button:disabled { opacity: 0.6; cursor: not-allowed; }
        .msg { font-size: 12px; font-family: var(--font-mono); }
        .msg.ok { color: var(--color-success); }
        .msg.err { color: #ff7a9a; }
      `}</style>
    </form>
  );
}
```

- [ ] **Step 3: Write Missions page**

Create `src/pages/missions.astro`:

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import MissionsForm from '../components/MissionsForm.tsx';
---

<BaseLayout title="For Missions" description="Commercial-grade ML runtime for satellite missions. Open-source orbit4ml powers the platform; the runtime makes it flight-ready.">
  <section class="missions">
    <div class="container inner">
      <div class="copy">
        <div class="micro-label">FOR MISSIONS</div>
        <h1>Flying ML on a real satellite?</h1>
        <p class="lede">
          <strong>orbit4ml</strong> is open, MIT-licensed, and free forever — great for research, prototyping, and learning. For flight-grade deployment on radiation-tolerant hardware, we're building a commercial runtime.
        </p>

        <h3>What the runtime adds</h3>
        <ul>
          <li>Deterministic scheduling that respects your mission profile's power & thermal envelope</li>
          <li>Fault-tolerant training with SEU-aware checkpoint/restart primitives</li>
          <li>Model compilation for radiation-hardened SoCs and FPGAs (Xilinx UltraScale+, NVIDIA Jetson Orin IR, etc.)</li>
          <li>Federated aggregation over inter-satellite links with topology-aware scheduling</li>
          <li>Support contracts with response times that match your mission clock</li>
        </ul>

        <h3>Who we work with</h3>
        <p>Satellite operators, space agencies, aerospace primes, and NewSpace startups with ML workloads in mission. If that's you — or you're planning it — let's talk.</p>
      </div>

      <aside class="form-card">
        <h3>Get in touch</h3>
        <p>Tell us about your mission. We'll reply within a week.</p>
        <MissionsForm client:visible />
        <p class="small">We don't send cold email. Your details stay with us.</p>
      </aside>
    </div>
  </section>
</BaseLayout>

<style>
  .missions { padding: var(--space-12) 0 var(--space-16); }
  .inner { display: grid; grid-template-columns: 1.3fr 1fr; gap: var(--space-10); align-items: start; }
  .copy h3 { margin-top: var(--space-8); }
  .lede { font-size: 16px; line-height: 1.6; max-width: 560px; }
  ul { padding-left: 1.2em; }
  ul li { margin-bottom: 8px; color: var(--color-text-secondary); font-size: 14px; }
  .form-card { padding: var(--space-6); background: var(--color-bg-elevated); border: 1px solid var(--color-border); border-radius: var(--radius-lg); position: sticky; top: 100px; }
  .form-card p { margin-bottom: var(--space-4); font-size: 13px; }
  .small { font-size: 11px; color: var(--color-text-muted); margin-top: var(--space-4); }
  @media (max-width: 1024px) { .inner { grid-template-columns: 1fr; } .form-card { position: static; } }
</style>
```

- [ ] **Step 4: Commit**

```bash
git add api/contact.ts src/components/MissionsForm.tsx src/pages/missions.astro
git commit -m "feat: add For Missions page with contact form and Formspree endpoint"
git push
```

---

### Task 27: Community page

**Files:**
- Create: `src/pages/community.astro`

- [ ] **Step 1: Write the page**

Create `src/pages/community.astro`:

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';

const channels = [
  {
    name: 'GitHub Discussions',
    desc: 'Questions, ideas, and showcase — async, threaded, searchable.',
    href: 'https://github.com/orbit-ml/orbit4ml/discussions',
    cta: 'Join discussions ↗',
  },
  {
    name: 'GitHub Issues',
    desc: 'Bug reports and feature requests.',
    href: 'https://github.com/orbit-ml/orbit4ml/issues',
    cta: 'Open an issue ↗',
  },
  {
    name: 'Pull Requests',
    desc: 'Code, docs, tutorials, examples — all welcome.',
    href: 'https://github.com/orbit-ml/orbit4ml/pulls',
    cta: 'See open PRs ↗',
  },
];
---

<BaseLayout title="Community" description="Get involved with orbit4ml and orbitalml.">
  <section class="community">
    <div class="container">
      <div class="head">
        <div class="micro-label">COMMUNITY</div>
        <h1>Build space ML with us.</h1>
        <p class="sub">orbit4ml is an open project. Everything happens on GitHub — no separate forum, no gated Slack.</p>
      </div>

      <div class="grid">
        {channels.map((c) => (
          <a class="card" href={c.href} target="_blank" rel="noopener noreferrer">
            <h3>{c.name}</h3>
            <p>{c.desc}</p>
            <span class="cta">{c.cta}</span>
          </a>
        ))}
      </div>

      <div class="contrib">
        <h3>How to contribute</h3>
        <ol>
          <li><code>git clone https://github.com/orbit-ml/orbit4ml.git</code></li>
          <li><code>pip install -e ".[dev]"</code></li>
          <li>Pick an issue labeled <code>good first issue</code></li>
          <li>Open a PR with tests and a tight commit message</li>
        </ol>
        <p>We review most PRs within a week. All contributions are MIT-licensed.</p>
      </div>

      <div class="coc">
        <h3>Code of Conduct</h3>
        <p>We follow the <a href="https://www.contributor-covenant.org/">Contributor Covenant</a>. Be kind, be constructive, assume good faith.</p>
      </div>
    </div>
  </section>
</BaseLayout>

<style>
  .community { padding: var(--space-12) 0 var(--space-16); }
  .head { max-width: 720px; margin-bottom: var(--space-12); }
  .sub { font-size: 16px; max-width: 560px; }
  .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-5); margin-bottom: var(--space-16); }
  .card { padding: var(--space-6); background: var(--color-bg-elevated); border: 1px solid var(--color-border); border-radius: var(--radius-lg); transition: border-color 0.15s, transform 0.15s; }
  .card:hover { border-color: var(--color-accent-blue); transform: translateY(-2px); color: var(--color-text-primary); }
  .card h3 { color: var(--color-text-primary); margin-bottom: var(--space-2); }
  .card p { font-size: 13px; margin-bottom: var(--space-3); }
  .cta { font-family: var(--font-mono); font-size: 11px; color: var(--color-accent-blue); }
  .contrib, .coc { max-width: 720px; margin-bottom: var(--space-10); }
  .contrib ol { padding-left: 1.2em; color: var(--color-text-secondary); font-size: 14px; line-height: 1.8; }
  @media (max-width: 1024px) { .grid { grid-template-columns: 1fr 1fr; } }
  @media (max-width: 640px) { .grid { grid-template-columns: 1fr; } }
</style>
```

- [ ] **Step 2: Commit**

```bash
git add src/pages/community.astro
git commit -m "feat: add community page with GitHub channels and contribution guide"
git push
```

---

## Phase 6: Quality Gates and Deploy

### Task 28: Playwright setup and smoke tests

**Files:**
- Create: `playwright.config.ts`, `tests/e2e/homepage.spec.ts`, `tests/e2e/tutorial.spec.ts`
- Modify: `package.json`, `.gitignore`

- [ ] **Step 1: Install Playwright**

```bash
npm install -D @playwright/test
npx playwright install --with-deps chromium
```

- [ ] **Step 2: Write the config**

Create `playwright.config.ts`:

```ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 60_000,
  retries: process.env.CI ? 2 : 0,
  use: {
    baseURL: 'http://localhost:4321',
    trace: 'on-first-retry',
  },
  projects: [
    { name: 'desktop', use: { ...devices['Desktop Chrome'], viewport: { width: 1280, height: 800 } } },
    { name: 'tablet',  use: { ...devices['Desktop Chrome'], viewport: { width: 1024, height: 800 } } },
    { name: 'mobile',  use: { ...devices['Desktop Chrome'], viewport: { width: 390, height: 780 } } },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:4321',
    reuseExistingServer: !process.env.CI,
    timeout: 60_000,
  },
});
```

- [ ] **Step 3: Write homepage smoke test**

Create `tests/e2e/homepage.spec.ts`:

```ts
import { test, expect } from '@playwright/test';

test('homepage renders hero and feature grid', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { level: 1 })).toContainText(/ML harness for the planet/i);
  await expect(page.getByRole('link', { name: /Try in browser/i })).toBeVisible();
  await expect(page.getByText('Simulate orbital constraints')).toBeVisible();
});

test('nav links work', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('link', { name: 'Learn' }).first().click();
  await expect(page).toHaveURL(/\/learn/);
  await expect(page.getByRole('heading', { level: 1 })).toContainText(/Interactive tutorials/i);
});
```

- [ ] **Step 4: Write Pyodide smoke test**

Create `tests/e2e/tutorial.spec.ts`:

```ts
import { test, expect } from '@playwright/test';

test('getting-started tutorial loads and runs first code cell', async ({ page }) => {
  await page.goto('/learn/getting-started');
  await expect(page.getByRole('heading', { level: 1 })).toContainText('Getting Started');

  const runButton = page.getByRole('button', { name: /Run ▶|Loading Pyodide…/ }).first();
  await runButton.click();

  // Pyodide + orbit4ml install may take up to 45s on a cold cache
  await expect(page.locator('.output').first()).toContainText('Total satellites: 66', { timeout: 60_000 });
});
```

- [ ] **Step 5: Add scripts**

Update `package.json` `scripts` block:

```json
"scripts": {
  "dev": "astro dev",
  "start": "astro dev",
  "build": "astro build",
  "preview": "astro preview",
  "astro": "astro",
  "check": "astro check",
  "test:e2e": "playwright test",
  "test:e2e:headed": "playwright test --headed"
}
```

Add to `.gitignore`:

```bash
echo 'test-results/
playwright-report/
.playwright/' >> .gitignore
```

- [ ] **Step 6: Run the tests locally**

```bash
npm run build && npm run test:e2e
```

Expected: 8 tests pass (2 tests × 3 viewports + 2 more × 1 viewport variant). Pyodide test may take 60s.

- [ ] **Step 7: Commit**

```bash
git add playwright.config.ts tests/ package.json package-lock.json .gitignore
git commit -m "test: add Playwright smoke tests for homepage nav and Pyodide execution"
git push
```

---

### Task 29: Link checker (lychee)

**Files:**
- Create: `.github/workflows/links.yml`, `lychee.toml`

- [ ] **Step 1: Write config**

Create `lychee.toml`:

```toml
max_concurrency = 8
retry_wait_time = 2
timeout = 20
accept = [200, 201, 204, 301, 302, 307, 308, 403, 429]
exclude = [
  "^https://fonts\\.googleapis\\.com",
  "^https://fonts\\.gstatic\\.com",
  "^http://localhost",
]
```

- [ ] **Step 2: Write workflow**

Create `.github/workflows/links.yml`:

```yaml
name: Links

on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: '0 6 * * 1'  # Monday 06:00 UTC

jobs:
  lychee:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run build
      - name: Link checker
        uses: lycheeverse/lychee-action@v2
        with:
          args: --config ./lychee.toml --verbose --no-progress ./dist
          fail: true
```

- [ ] **Step 3: Commit**

```bash
git add lychee.toml .github/workflows/links.yml
git commit -m "ci: add lychee link checker on push, PR, and weekly schedule"
git push
```

---

### Task 30: Build + typecheck + test CI

**Files:**
- Create: `.github/workflows/ci.yml`

- [ ] **Step 1: Write workflow**

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run check
      - run: npm run build

  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - name: Install Playwright browsers
        run: npx playwright install --with-deps chromium
      - run: npm run build
      - run: npm run test:e2e
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 14
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "ci: add build + typecheck + Playwright workflow"
git push
```

---

### Task 31: Lighthouse CI

**Files:**
- Create: `.github/workflows/lighthouse.yml`, `lighthouserc.json`

- [ ] **Step 1: Write Lighthouse config**

Create `lighthouserc.json`:

```json
{
  "ci": {
    "collect": {
      "staticDistDir": "./dist",
      "url": [
        "http://localhost/index.html",
        "http://localhost/learn/index.html",
        "http://localhost/benchmarks/index.html"
      ],
      "numberOfRuns": 2
    },
    "assert": {
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.9 }],
        "categories:accessibility": ["error", { "minScore": 0.95 }],
        "categories:best-practices": ["warn", { "minScore": 0.9 }],
        "categories:seo": ["warn", { "minScore": 0.9 }]
      }
    },
    "upload": {
      "target": "temporary-public-storage"
    }
  }
}
```

- [ ] **Step 2: Write workflow**

Create `.github/workflows/lighthouse.yml`:

```yaml
name: Lighthouse

on:
  pull_request:
  push:
    branches: [main]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - name: Run Lighthouse CI
        run: |
          npm install -g @lhci/cli@0.14.x
          lhci autorun
        env:
          LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}
```

- [ ] **Step 3: Commit**

```bash
git add lighthouserc.json .github/workflows/lighthouse.yml
git commit -m "ci: add Lighthouse CI with performance and a11y budgets"
git push
```

---

### Task 32: Deploy to Vercel

**Files:**
- Create: `vercel.json`

- [ ] **Step 1: Write Vercel config**

Create `vercel.json`:

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "astro",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "cleanUrls": true,
  "trailingSlash": false,
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "SAMEORIGIN" },
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" }
      ]
    }
  ]
}
```

- [ ] **Step 2: Commit**

```bash
git add vercel.json
git commit -m "chore: add vercel.json with framework preset and security headers"
git push
```

- [ ] **Step 3: Manual — connect to Vercel**

The human performs these steps (one-time setup, not scripted):

1. Go to https://vercel.com/new
2. Import the `orbit-ml/orbitalml` repo
3. Framework preset: **Astro** (auto-detected)
4. Environment variables to add:
   - `BUTTONDOWN_API_KEY` = (from Buttondown dashboard)
   - `FORMSPREE_FORM_ID` = (from Formspree dashboard)
   - `PUBLIC_PLAUSIBLE_DOMAIN` = `orbitalml.com`
5. Click **Deploy**
6. Once live, add custom domain `orbitalml.com` in Vercel → Settings → Domains
7. Update DNS at the domain registrar per Vercel's instructions (typically an A record and a CNAME)

- [ ] **Step 4: Verify deploy**

Once DNS propagates, visit `https://orbitalml.com` and confirm:
- Homepage renders with hero animation
- Nav works, all 7 sections load
- `/learn/getting-started` runs a Pyodide code block
- Newsletter signup POSTs to `/api/subscribe` successfully
- Missions form POSTs to `/api/contact` successfully

---

### Task 33: Add Plausible analytics

**Files:**
- Modify: `src/layouts/BaseLayout.astro`

- [ ] **Step 1: Add script**

In `src/layouts/BaseLayout.astro`, add inside the `<head>` (after the canonical link):

```astro
{import.meta.env.PUBLIC_PLAUSIBLE_DOMAIN && (
  <script
    is:inline
    defer
    data-domain={import.meta.env.PUBLIC_PLAUSIBLE_DOMAIN}
    src="https://plausible.io/js/script.js"
  ></script>
)}
```

- [ ] **Step 2: Commit**

```bash
git add src/layouts/BaseLayout.astro
git commit -m "feat: add Plausible analytics when PUBLIC_PLAUSIBLE_DOMAIN is set"
git push
```

---

### Task 34: README + launch checklist

**Files:**
- Modify: `README.md`
- Create: `LAUNCH.md`

- [ ] **Step 1: Expand README**

Overwrite `README.md`:

```markdown
# orbitalml

The interactive showcase site for [orbit4ml](https://github.com/orbit-ml/orbit4ml).

> ML harness for the planet.

## Develop

```bash
npm install
npm run dev       # http://localhost:4321
```

## Quality gates

```bash
npm run check     # TypeScript + Astro type check
npm run build     # Production build
npm run test:e2e  # Playwright smoke tests
```

## Deploy

Automatic via Vercel on push to `main`.

Preview deploys run on every PR. See Vercel dashboard for URLs.

## Environment variables

See `.env.example`. Required for production:

- `BUTTONDOWN_API_KEY` — newsletter subscriptions
- `FORMSPREE_FORM_ID` — missions contact form
- `PUBLIC_PLAUSIBLE_DOMAIN` — analytics (optional; falls back to no analytics)

## Tech stack

- Astro 4.x, React 18, TypeScript
- Pyodide for in-browser Python tutorials
- JupyterLite for the Playground
- three.js + react-three-fiber for the hero constellation
- Vercel for hosting + serverless API routes

## Content authoring

- Tutorials live in `src/content/tutorials/*.mdx`
- Blog posts live in `src/content/blog/*.mdx`
- Design tokens are in `src/styles/tokens.css`

## License

MIT. See `LICENSE`.
```

- [ ] **Step 2: Write LAUNCH.md**

Create `LAUNCH.md`:

```markdown
# Launch Checklist

One-time steps to take orbitalml v1 live.

## DNS & domain
- [ ] Register `orbitalml.com` at a registrar
- [ ] Add custom domain in Vercel project
- [ ] Add A/CNAME records per Vercel instructions
- [ ] Verify SSL is issued (Vercel auto-issues Let's Encrypt)

## Env vars (Vercel → Project → Settings → Environment Variables)
- [ ] `BUTTONDOWN_API_KEY` (from buttondown.email → Settings → API)
- [ ] `FORMSPREE_FORM_ID` (from formspree.io → New form)
- [ ] `PUBLIC_PLAUSIBLE_DOMAIN` = `orbitalml.com`

## Analytics
- [ ] Create Plausible site for `orbitalml.com`
- [ ] Verify Plausible is receiving events after deploy

## Pre-launch verification
- [ ] `/` loads, hero animates, stats line shows
- [ ] `/learn` lists 3 tutorials in order
- [ ] `/learn/getting-started` Pyodide block prints "Total satellites: 66"
- [ ] `/playground` iframe loads JupyterLite
- [ ] `/blog` lists 2 posts
- [ ] `/benchmarks` shows 4 metric cards
- [ ] `/missions` form submits successfully (real email arrives)
- [ ] Newsletter signup on `/` succeeds (subscriber appears in Buttondown)
- [ ] Lighthouse CI passes on main
- [ ] `/community` links all resolve to GitHub

## Launch
- [ ] Merge `main` → production deploy
- [ ] Announce on GitHub Discussions
- [ ] Post launch blog post link to relevant communities (HackerNews, /r/space, space-ML Slack groups, Twitter/X)
- [ ] Update `orbit4ml` README with "See the interactive tutorials at orbitalml.com"

## Post-launch (week 1)
- [ ] Watch for 404s in Vercel logs — fix broken links
- [ ] Monitor Pyodide bundle load times — optimize if >10s p95
- [ ] Review first subscribers/contacts — follow up with missions inquiries
```

- [ ] **Step 3: Commit**

```bash
git add README.md LAUNCH.md
git commit -m "docs: expand README and add launch checklist"
git push
```

---

## Self-Review Notes

After writing this plan, I checked it against the spec:

**Spec coverage:**
- ✅ Name / tagline / sub-copy — Task 7 (Hero)
- ✅ Visual direction (tokens, motifs, telemetry tooltips, hero viz) — Tasks 2, 6, 7
- ✅ All 7 top-level sections — Tasks 4, 11, 19, 20, 22, 25, 26, 27
- ✅ Pyodide + JupyterLite + Colab blend — Tasks 12, 16–20; Colab link is in Task 18
- ✅ Astro + React + Vercel stack — Tasks 1, 10, 32
- ✅ In-scope items all present (homepage, 3 tutorials, playground, blog, benchmarks, missions, community, mobile breakpoints, dark theme, custom domain) — verified per section
- ✅ Testing: Playwright visual/functional + Lighthouse + link checker — Tasks 28–31
- ✅ Analytics: Plausible — Task 33
- ✅ Newsletter (Buttondown) + Contact (Formspree) — Tasks 10, 26

**Non-coverage (intentionally deferred per spec):** accounts, user-submitted benchmarks, self-hosted forum, certificates, offline mode, multi-lang. None of these appear in this plan.

**Placeholder scan:** No "TBD", no "implement later", no "similar to Task N". Every step has the actual code or command.

**Type consistency:** `CodeRunner` exposes `{initial, height}` (Task 12), used as `<CodeRunner client:visible initial={...} />` (Task 16) and `<CodeRunner client:visible height={...} initial={...} />` (Task 17) — consistent. `NewsletterSignup` accepts `{inline}` (Task 9), used as `<NewsletterSignup client:visible inline={true} />` (Task 11) — consistent.

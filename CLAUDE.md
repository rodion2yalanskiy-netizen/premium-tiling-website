# CLAUDE.md — QSNera Website

This file provides Claude Code with essential context about the QSNera project structure, conventions, and workflows.

---

## Project Overview

**QSNera** is a luxury tile and stone installation studio. This is a high-end, single-page marketing website showcasing premium services: bookmatched marble slab fabrication, large-format porcelain tiling, and handcrafted Zellige installations for residential and commercial estates.

**Tech stack:** Vanilla HTML5 + CSS3 + JavaScript (no frameworks, no build tools, no dependencies).
All code lives in a single `index.html` file — styles in `<style>`, scripts at the bottom in `<script>`.

---

## Directory Structure

```
premium-tiling-website/
├── index.html              # Entire website: markup, CSS, and JS in one file
├── assets/
│   ├── hero-bg.png         # Hero background / marble texture (used for bookmatch effect)
│   ├── portfolio-1.png     # Portfolio gallery image
│   ├── portfolio-2.png     # Portfolio gallery image
│   ├── portfolio-3.png     # Portfolio gallery image
│   └── portfolio-4.png     # Portfolio gallery image
├── Q&A/
│   ├── CLAUDE_TASK.md      # Detailed frontend technical specification (task history)
│   └── QSNera_Content.md   # Content brief / copywriting source
├── Obsidian Vault/         # Personal project notes (Obsidian, not part of the website)
├── .gitignore
└── CLAUDE.md               # This file
```

---

## Running the Project

This is a static website with zero dependencies — no npm, no build step, no server required.

### Open locally
```bash
# macOS — open in default browser directly
open index.html

# Or with a local dev server (Python, no install required)
python3 -m http.server 8080
# Then visit: http://localhost:8080
```

### Live preview (recommended for development)
Use VS Code with the **Live Server** extension, or any static file server. The site works identically from the filesystem or a server.

---

## Design System (CSS Variables)

All visual tokens are defined in `:root` at the top of the `<style>` block. **Never hardcode colors or fonts — always use variables.**

| Variable | Value | Usage |
|---|---|---|
| `--color-charcoal-dark` | `#0d0d0d` | Main page background |
| `--color-charcoal-mid` | `#161618` | Alternate section background |
| `--color-charcoal-light` | `#222224` | Cards, elevated surfaces |
| `--color-gold-matte` | `#c5a880` | Primary accent, borders |
| `--color-gold-bright` | `#e5cda8` | Highlights, hover states |
| `--color-gold-dark` | `#8c7352` | Subdued gold accents |
| `--color-white` | `#f5f5f7` | Body text |
| `--color-gray-text` | `#a1a1a6` | Secondary text |
| `--color-gold-border` | `rgba(197,168,128,0.15)` | Subtle dividers |
| `--font-serif` | Playfair Display | Headings, display text |
| `--font-sans` | Outfit | Body text, UI labels |
| `--transition-smooth` | `0.6s cubic-bezier(0.16,1,0.3,1)` | Section-level animations |
| `--transition-fast` | `0.3s cubic-bezier(0.16,1,0.3,1)` | Hover/interactive transitions |

---

## Page Sections (in order)

| Section ID | Description |
|---|---|
| `#hero` | Full-screen hero with animated headline |
| `#expertise` | Three core expertise cards |
| `#portfolio` | 4-image portfolio gallery grid |
| `#marble-showcase` | Interactive bookmatched marble widget |
| `#philosophy` | Studio philosophy text block |
| `#services` | Detailed services list |
| `#testimonials` | Client testimonial quotes |
| `#contact` | Contact form and studio details |

Sections alternate between `--color-charcoal-dark` and `--color-charcoal-mid` backgrounds.
All sections use the `.reveal` class and are animated in via `IntersectionObserver` on scroll.

---

## Coding Rules

### General
- **No external libraries.** Do not add jQuery, Bootstrap, GSAP, or any npm package. The project is intentionally dependency-free.
- **No inline styles on new elements.** Use CSS classes. Inline `style=""` attributes only exist in legacy markup — do not add new ones.
- **All new CSS goes in the `<style>` block**, grouped under a clearly labelled comment block:
  ```css
  /* ==========================================================================
     SECTION NAME
     ========================================================================== */
  ```
- **All new JS goes in the `<script>` block** at the bottom of `index.html`, near related interactive code.

### CSS
- Use CSS custom properties for every color, font, and transition value.
- Mobile-first is NOT used — desktop-first with `max-width` breakpoints. Primary breakpoint: `992px`.
- Responsive collapse for grid layouts: `grid-template-columns: 1fr` at `max-width: 992px`.
- Animations use `@keyframes` + `IntersectionObserver`. Do not use scroll-linked JS listeners.

### JavaScript
- Pure ES6+ (no transpilation). Use `const`/`let`, arrow functions, template literals.
- DOM queries with `document.getElementById` or `document.querySelector`.
- Always guard DOM queries: `if (element) { ... }` before attaching event listeners.
- No `console.log` in committed code.

### HTML
- Semantic elements: `<section>`, `<nav>`, `<header>`, `<footer>`, `<article>`.
- New sections must include: `id=""`, `class="... reveal"` for scroll animation.
- Brand name: **QSNera** (not AURELIA, not Aurelia, not QSnera — respect the exact casing).
- Contact email: `inquire@qsnera.com`

---

## UI/UX & Design Guidelines

> **Mandatory checklist for every frontend change.**
> Before committing any modification to `index.html` (markup, styles, or scripts), Claude must verify all four areas below.

### 1. Responsiveness
- Test every new layout at the primary breakpoint (`max-width: 992px`) — grids must collapse to a single column cleanly.
- Check at three viewport widths: **375px** (mobile), **768px** (tablet), **1440px** (desktop).
- No horizontal scroll at any breakpoint (`overflow-x: hidden` is set globally — do not break it).
- Touch targets (buttons, links) must be at least **44×44 px** on mobile.
- Text must remain legible (no overflow, no clipping) at all sizes.

### 2. Luxury Brand Compliance
- **Every visual decision must feel premium.** QSNera targets high-end residential and commercial clients — nothing should look generic, cheap, or misaligned with the dark-gold aesthetic.
- **Color:** Only use tokens from the Design System table. Never introduce new colors outside `:root`.
- **Typography:** Headings → `--font-serif` (Playfair Display). Body/UI → `--font-sans` (Outfit). No other fonts.
- **Spacing:** Sections use `padding: 10rem 0` on desktop, `6rem 0` on mobile — maintain this scale.
- **Borders & dividers:** Always `1px solid var(--color-gold-border)` — never solid opaque borders.
- **Imagery:** Assets are high-res stone/marble textures. Do not resize, compress, or replace without approval.
- **Tone of UI copy:** Uppercase labels, wide letter-spacing (`letter-spacing: 0.1em`+), restrained punctuation. No playful or casual language.

### 3. Accessibility (a11y)
- All `<img>` elements must have a descriptive `alt` attribute.
- Interactive elements (`<button>`, `<a>`) must be keyboard-focusable and have visible `:focus-visible` styles.
- Color contrast ratio must meet **WCAG AA** minimum: 4.5:1 for body text, 3:1 for large text/UI components. Gold on dark backgrounds already passes — verify any new color combination.
- Use semantic HTML: `<button>` for actions, `<a>` for navigation. Never use `<div>` as a click target.
- Form inputs in `#contact` must have associated `<label>` elements.
- Do not remove or override `aria-*` attributes without an explicit reason.

### 4. Animation Quality
- All transitions must use the design system easing: `cubic-bezier(0.16, 1, 0.3, 1)` — this is a premium ease-out curve, not linear or ease-in-out.
- Duration: `--transition-fast` (0.3s) for hover states; `--transition-smooth` (0.6s) for section/layout animations.
- Scroll-reveal: use the existing `IntersectionObserver` + `.reveal` class. Do not add scroll event listeners.
- Animations must respect `prefers-reduced-motion`:
  ```css
  @media (prefers-reduced-motion: reduce) {
    /* disable or simplify animation */
  }
  ```
- No jank: avoid animating `width`, `height`, `top`, `left`. Animate `transform` and `opacity` only.
- The pulsing `.seam-pulse` and scroll-reveal timing must not be disrupted by new CSS additions.

---

## Key Interactions

### Scroll Reveal Animation
All `.reveal` elements animate in when they enter the viewport. Managed by `IntersectionObserver` — do not modify this system.

### Bookmatched Marble Widget (`#marble-showcase`)
- Two CSS slabs display the same `assets/hero-bg.png`; the right slab uses `transform: scaleX(-1)` to create a mirrored book-match effect.
- Toggle buttons (`#btn-align-yes` / `#btn-align-no`) add/remove the `.misaligned` class on `#marble-slab-wall`.
- `.misaligned .slab-right` applies `transform: scaleX(-1) translateY(-60px)` to break alignment.

---

## Git Workflow

```bash
git status
git add -A
git commit -m "feat: <short description>"
```

There is no CI/CD pipeline. The site is deployed by copying files to a static host.

---

## Content Reference

- **Full technical spec:** `Q&A/CLAUDE_TASK.md`  
- **Copy brief:** `Q&A/QSNera_Content.md`  
- **Personal project notes:** `Obsidian Vault/`

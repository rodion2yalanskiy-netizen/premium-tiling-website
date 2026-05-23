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
│   ├── hero-bg.png         # Hero background / marble texture
│   ├── portfolio-1.png     # Portfolio gallery image
│   ├── portfolio-2.png     # Portfolio gallery image
│   ├── portfolio-3.png     # Portfolio gallery image
│   └── portfolio-4.png     # Portfolio gallery image
├── Q&A/
│   ├── CLAUDE_TASK.md      # Detailed frontend technical specification
│   └── QSNera_Content.md   # Content brief / copywriting source
├── Obsidian Vault/         # Personal project notes (not part of the website)
├── .gitignore
└── CLAUDE.md               # This file
```

---

## Running the Project

```bash
open index.html
# or
python3 -m http.server 8080
```

---

## Design System (CSS Variables)

All visual tokens are defined in `:root`. **Never hardcode colors or fonts — always use variables.**

### Color Palette — Dark Navy + Copper-Gold + Warm Cream

Updated: May 2026 — based on trust+premium research. Variants 4 (Copper/warm) and 5 (Purple gradient) merged.

| Variable | Value | Usage |
|---|---|---|
| `--color-bg-dark` | `#0D1B2E` | Main page background (deep navy) |
| `--color-bg-mid` | `#0F2035` | Alternate section background |
| `--color-bg-card` | `#152845` | Cards, elevated surfaces |
| `--color-bg-accent` | `#1A1035` | Purple-tinted accent sections |
| `--color-copper` | `#C8903A` | Primary accent, borders (copper-gold) |
| `--color-copper-bright` | `#E8B86D` | Highlights, hover states |
| `--color-copper-dark` | `#8A6028` | Subdued accent |
| `--color-indigo` | `#4F46E5` | CTA buttons, key actions |
| `--color-indigo-hover` | `#6366F1` | Button hover state |
| `--color-cream` | `#F5ECD7` | Body text (warm cream) |
| `--color-cream-dim` | `#B8A99A` | Secondary text |
| `--color-border` | `rgba(200,144,58,0.18)` | Subtle dividers |
| `--font-serif` | Playfair Display | Headings, display text |
| `--font-sans` | Outfit | Body text, UI labels |
| `--transition-smooth` | `0.6s cubic-bezier(0.16,1,0.3,1)` | Section-level animations |
| `--transition-fast` | `0.3s cubic-bezier(0.16,1,0.3,1)` | Hover/interactive transitions |

### Typography Scale

| Use | Font | Weight | Letter-spacing |
|---|---|---|---|
| Hero H1 | Playfair Display | 700 | -0.02em |
| Section H2 | Playfair Display | 600 | 0 |
| Card H3 | Outfit | 600 | 0.05em |
| Body | Outfit | 400 | 0 |
| Labels/Tags | Outfit | 500 | 0.12em uppercase |
| CTA buttons | Outfit | 600 | 0.08em uppercase |

---

## Ideal Page Structure (Client-Oriented)

**Core principle:** User decides to trust in 0.05 seconds. Structure guides from CLIENT PAIN → OUR SOLUTION → PROOF → ACTION.

Every section must answer: *"What does the client get?"* — not *"What do we offer?"*

### Required sections in order:

| # | Section ID | Purpose | Client-Oriented Rule |
|---|---|---|---|
| 1 | `#hero` | Hook — benefit-first headline | H1 must describe client benefit, not company name |
| 2 | `#trust-bar` | Quick trust signals | Real numbers only — proof not vague claims |
| 3 | `#services` | What problems we solve | Start with client pain point, then solution |
| 4 | `#portfolio` | Visual proof | Real work, real results — no stock photos |
| 5 | `#why-us` | Differentiators | Honest comparison, no "best/fastest/cheapest" |
| 6 | `#process` | How it works | Reduce anxiety — show clear numbered steps |
| 7 | `#testimonials` | Social proof | Real names, specific results, real locations |
| 8 | `#faq` | Remove objections | Answer real questions clients ask |
| 9 | `#cta` | One clear action | Single dominant CTA — no competing buttons |
| 10 | `#contact` | Conversion | Max 4 fields — each extra field = -10% conversion |

### CTA Rules

- Primary CTA: specific result → **"Get a Free Estimate"** not "Contact Us"
- Secondary CTA: **"View Our Work"** not "Learn More"
- Every page section must have a visible path to the primary CTA
- Mobile: sticky bottom bar with primary CTA always visible

### Trust Signal Rules

- Use real numbers: "127 completed projects" not "many projects"
- Testimonials: full name + location + specific result
- Certifications: show badge/logo, not just text
- Never: "best in class", "industry leading", "we fix everything"

---

## Page Sections (current implementation)

| Section ID | Description |
|---|---|
| `#hero` | Full-screen hero — benefit-first headline + dual CTA |
| `#trust-bar` | 4 trust numbers (projects, years, satisfaction, response) |
| `#services` | Three core services as problem→solution cards |
| `#portfolio` | 4-image portfolio gallery grid |
| `#why-us` | Differentiators + honest positioning + stat grid |
| `#process` | 4-step service process |
| `#testimonials` | Client testimonial quotes with names and locations |
| `#faq` | Accordion FAQ — 6 common questions |
| `#cta` | Final CTA band — single action |
| `#contact` | Minimal contact form (4 fields max) |

---

## Coding Rules

### General
- **No external libraries.** No jQuery, Bootstrap, GSAP, npm packages. Zero dependencies.
- **No inline styles on new elements.** Use CSS classes only.
- **All new CSS goes in the `<style>` block**, grouped under labelled comment blocks.
- **All new JS goes in the `<script>` block** at the bottom of `index.html`.

### CSS
- Use CSS custom properties for every color, font, and transition value.
- Desktop-first with `max-width` breakpoints. Primary breakpoint: `992px`.
- Responsive collapse: `grid-template-columns: 1fr` at `max-width: 992px`.
- Animations use `@keyframes` + `IntersectionObserver`. No scroll-linked JS listeners.

### JavaScript
- Pure ES6+. Use `const`/`let`, arrow functions, template literals.
- Guard all DOM queries: `if (element) { ... }` before attaching event listeners.
- No `console.log` in committed code.

### HTML
- Semantic elements: `<section>`, `<nav>`, `<header>`, `<footer>`, `<article>`.
- New sections: `id=""`, `class="... reveal"` for scroll animation.
- Brand name: **QSNera** (exact casing — not QSNERA, not QSnera).
- Contact email: `inquire@qsnera.com`

---

## UI/UX & Design Guidelines

> **Mandatory checklist before every commit to `index.html`.**

### 1. Responsiveness
- Test at: **375px** (mobile), **768px** (tablet), **1440px** (desktop)
- No horizontal scroll at any breakpoint
- Touch targets minimum **44×44 px** on mobile
- Sticky mobile CTA bar must always be visible on mobile

### 2. Premium Brand Compliance
- Every decision must feel premium — QSNera targets high-end residential and commercial clients
- **Color:** Only tokens from Design System table. No hardcoded values.
- **Typography:** Headings → `--font-serif`. Body/UI → `--font-sans`. No other fonts.
- **Spacing:** Sections `padding: 8rem 0` desktop, `6rem 0` mobile
- **Borders:** Always `1px solid var(--color-border)` — never solid opaque
- **Primary buttons:** `--color-indigo`. **Accent elements:** `--color-copper`.

### 3. Client-Oriented Checklist (May 2026)
Before publishing any section, verify:
- [ ] Headline describes client benefit, not company feature
- [ ] CTA says what the client gets ("Get estimate" not "Submit")
- [ ] Trust signals use real numbers, not vague claims
- [ ] No fake testimonials, no stock photos of people
- [ ] Form has 4 fields or fewer
- [ ] Page has one dominant CTA — no competing buttons

### 4. Accessibility (a11y)
- All `<img>` must have descriptive `alt`
- Interactive elements must be keyboard-focusable with visible `:focus-visible`
- WCAG AA contrast: 4.5:1 for body, 3:1 for large text/UI
- `<button>` for actions, `<a>` for navigation — never `<div>` as click target
- Form inputs must have associated `<label>` elements

### 5. Animation Quality
- Easing: `cubic-bezier(0.16, 1, 0.3, 1)` — premium ease-out only
- Duration: `--transition-fast` (0.3s) hover; `--transition-smooth` (0.6s) layout
- Scroll-reveal: existing `IntersectionObserver` + `.reveal` class
- Must respect `prefers-reduced-motion`
- Animate only `transform` and `opacity` — never width/height/top/left

---

## Token Efficiency Rules

> Apply these in every session to keep context lean and responses fast.

- Reply concisely — no explanations unless asked
- Never repeat entire files — show only changed functions (diff-format)
- For large files, output only the modified block with surrounding context (~10 lines)
- Write pseudocode / bullet plan first, then generate full code
- Ask clarifying questions before generating — one round of questions saves many rounds of regeneration
- Use `/compact` in Claude Code to compress context when token count grows
- Break large tasks into small focused sessions; store state in files, not context

---

## QA Testing Checklist

> Run through this before every PR / deployment of `index.html`.

### Functionality
- [ ] All buttons are clickable and respond correctly
- [ ] Contact form validates (required fields, email format) and submits
- [ ] Nav links scroll to correct sections
- [ ] FAQ accordion opens / closes
- [ ] Mobile menu works (hamburger → overlay)

### Visual / Layout
- [ ] No broken images (all `assets/` files load)
- [ ] No text overflow at any breakpoint
- [ ] Consistent spacing and typography across sections
- [ ] Correct render at **375px** mobile
- [ ] Correct render at **768px** tablet
- [ ] Correct render at **1440px** desktop
- [ ] No horizontal scroll at any breakpoint

### Performance
- [ ] Lighthouse score > 80 on all metrics (Performance, Accessibility, SEO, Best Practices)
- [ ] No errors in browser console
- [ ] Images are optimised (no raw PNGs > 500 KB)

### Accessibility
- [ ] All `<img>` have descriptive `alt` text
- [ ] Keyboard navigation works (Tab / Enter / Space)
- [ ] Color contrast meets WCAG AA (4.5:1 body, 3:1 large text)
- [ ] All form inputs have associated `<label>` elements
- [ ] Focus outlines visible on interactive elements

---

## Autonomous Code Quality — Auto-Check After Every Change

> Run ALL of these after modifying `index.html`. Fix every error before committing.

### 1. HTML Validation
```bash
npx htmlhint index.html
# Must output: "0 problems"
```

### 2. CSS Check (inline styles are valid here — skip file check)
```bash
# Check for forbidden hardcoded values (no #hex or rgb() outside :root)
grep -n "color: #\|color: rgb\|font-family: ['\"]" index.html | grep -v ":root" | grep -v "var(--"
# Must output nothing (empty = OK)
```

### 3. JavaScript Syntax Check
```bash
node --check index.html 2>/dev/null || \
  grep -o '<script[^>]*>.*</script>' index.html | node --input-type=module 2>&1 | head -5
```

### 4. Lighthouse Audit (run after `python3 -m http.server 8080`)
```bash
npx lighthouse http://localhost:8080 --only-categories=performance,accessibility,seo,best-practices \
  --output=json --quiet 2>/dev/null | python3 -c "
import json,sys; d=json.load(sys.stdin)
cats = d['categories']
for k,v in cats.items():
    score = int(v['score']*100)
    flag = '✅' if score>=80 else '❌'
    print(f'{flag} {k}: {score}')
"
```

### 5. Accessibility Check
```bash
npx axe http://localhost:8080 --exit 2>/dev/null | tail -5
```

### Self-Verification Protocol
Before every commit, Claude MUST:
1. Run htmlhint — fix any errors found
2. Check no hardcoded colors outside `:root`
3. Confirm all new `<img>` have `alt` attributes
4. Verify no new `console.log` statements added
5. Test that JS has no syntax errors

---

## Autonomous Problem Solving

When blocked on a task, use this sequence (without asking the user):
1. Re-read CLAUDE.md for constraints
2. Check existing code patterns in `index.html` for reference
3. Try the simplest solution first
4. If an approach fails, try the next one
5. Only report back when task is **done** or truly **impossible**

---

## Git Workflow

```bash
git status
git add -A
git commit -m "feat: <short description>"
```

---

## Content Reference

- **Full technical spec:** `Q&A/CLAUDE_TASK.md`
- **Copy brief:** `Q&A/QSNera_Content.md`
- **Design research:** `Obsidian Vault/Бизнес QSNera/QSNera — Сайт/Цветовые палитры — исследование.md`
- **Client-oriented principles:** `Obsidian Vault/Цифровой мозг/Ресурсы/Клиентоориентированный сайт — принципы.md`

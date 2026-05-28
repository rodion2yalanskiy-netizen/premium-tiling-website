# CLAUDE.md — Axiom:Void Website

This file provides Claude Code with essential context about the Axiom:Void website project.

---

## Project Overview

**Axiom:Void** is a web studio founded by Rodion Yalanskiy.
Services: Void:Form (UI/UX), Axiom:Core (backend), The Nexus (AI/API), Absolute Zero (audit).

**Website:** axiom-void.dev
**Tech stack:** Vanilla HTML5 + CSS3 + JavaScript (no frameworks, no build tools, no dependencies).
All code lives in a single `index.html` — styles in `<style>`, scripts at the bottom in `<script>`.

---

## Design System

```
Background:  #000000
Accent:      #00D4FF  (var(--color-accent))
Text:        #E8E8E8  (var(--color-text))
Surface:     #111111  (var(--color-surface))
Border:      #1A1A1A  (var(--color-border))

Fonts:       JetBrains Mono (headings, code), Inter (body)
Style:       strict minimalism, architect tone
Effects:     IntersectionObserver scroll-reveal, prefers-reduced-motion
```

---

## Directory Structure

```
premium-tiling-website/
├── index.html              # Entire website: markup, CSS, JS in one file
├── assets/
│   ├── hero-bg.png         # Hero section background
│   └── portfolio-*.png     # Portfolio images (1–14)
├── scripts/
│   ├── antigravity.py      # Antigravity pipeline integration
│   └── save_report.py      # Report saving utility
├── .github/workflows/
│   ├── agent-pipeline.yml  # AI agent pipeline
│   └── code-quality.yml    # Code quality checks
└── CLAUDE.md               # This file
```

---

## Key Rules

- `git add -A` always
- `git pull --rebase` before push
- Commit prefix: `feat:` / `fix:` / `refactor:`
- Reports: `Отчёт - Название.md`

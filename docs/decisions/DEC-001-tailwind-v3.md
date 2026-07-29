# DEC-001 — Tailwind CSS v3 (not v4) for the MVP frontend

Date: 2026-07-23 · Status: accepted

**Decision:** Use Tailwind CSS v3 (with the classic `tailwind.config.ts` + PostCSS
setup) for the MVP, not the newer v4.

**Context:** Story 0.1 initialized the Next.js + shadcn/ui frontend. Tailwind v4
exists and is faster, but changes the configuration model (CSS-first, `@theme`).

**Reason:** shadcn/ui's most-documented, most-stable path today is Tailwind v3.
For a solo founder optimizing for maintainability and copy-paste-able answers,
the well-trodden path beats the newer one. Zero learning tax.

**Tradeoffs:** We forgo v4's build-speed and CSS-first config. Migration later is
a known, bounded task (config + globals.css changes).

**Revisit when:** shadcn/ui's default guidance moves to v4, or build performance
becomes a real annoyance.

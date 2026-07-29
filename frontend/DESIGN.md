# Design System

The frontend is built as a **premium SaaS product** (target feel: Linear · Vercel ·
Stripe · Notion), not an internal admin panel. Every screen composes the shared
components below — we never write page-specific styling. When a page needs something
new, it becomes a reusable component here first.

## Principles
- **Calm & spacious.** Whitespace over borders; elevation over heavy outlines; rounded
  (12px) corners. Every page: title → description → primary action → content.
- **One accent.** Neutral slate surfaces + a single indigo primary, used sparingly.
- **Intentional motion.** 150–250ms, gentle ease. Fade/lift, staggered lists, subtle
  button/hover states. Never bouncy, never slow.
- **Backend is the source of truth.** The UI submits typed DTOs and *surfaces* the
  backend's verdicts (incl. error codes). It never re-implements business rules; client
  validation exists only for immediate UX feedback.
- **Every state is designed.** Loading = skeletons. Empty = icon + explanation + CTA.
  Error = human message + retry + correlation id. Never a blank page or a raw JSON dump.
- **Primary CTA (required).** Every page has exactly one clear primary action — the user
  should never wonder "what do I do next?" (List → Create; Detail → Invite; …).
- **Information density.** Important pages don't degrade to Title → Toolbar → Table. They
  answer three questions in order: **What happened? · What needs attention? · What next?**
  (A detail page grows toward: header/counts → "needs attention" → pipeline → activity →
  configuration — not just a bigger table.)
- **AI has its own language.** AI-produced content never looks like an ordinary field or a
  bare number. See `components/ai/README.md` (design contract; implemented in Epic 5).

## Tokens (`app/globals.css`, mapped in `tailwind.config.ts`)
HSL CSS variables, light + dark (driven by `next-themes`, `class` strategy):
`background · foreground · card · popover · primary · secondary · muted · accent ·
destructive · success · warning · border · input · ring`, plus `--radius: 0.75rem`.
Shadows: `shadow-subtle`, `shadow-elevated`. Font: **Geist** (`font-sans`).

## Components
- **`components/ui/`** — primitives: `Button` (variants primary/secondary/outline/ghost/
  destructive · sizes · `loading`), `Input`, `Textarea`, `Label`, `Card` (+Header/Title/
  Description/Content/Footer), `Badge` (neutral/primary/success/warning/outline), `Skeleton`.
- **`components/forms/`** — `Field` (label + control + hint/error). Forms use
  **React Hook Form + Zod**.
- **`components/layout/`** — `AppShell` (authenticated top nav: brand · Dashboard/Campaigns ·
  theme · logout — top-nav retained over a sidebar while destinations are few; `NAV` array is
  the single source of truth so a sidebar migration is a render change), `AuthShell` (centered
  auth frame), `CandidateShell` (candidate boundary — no nav/account, calm & trustworthy,
  mobile-first), `PageHeader`, `Stat` (headline metric; `attention` tone).
- **`components/ui/`** also includes `Dialog` (Radix-based modal).
- **`components/feedback/`** — `EmptyState`, `ErrorState`. Toasts via **Sonner** (`toast`).
- **`components/motion/`** — `FadeIn`, `StaggerList`, `StaggerItem` (Motion).
- **`components/theme/`** — `ThemeToggle`.
- **`components/status-badge.tsx`** — maps a campaign lifecycle state to a `Badge` tone.

## Libraries
Standardized: Next.js · TypeScript · Tailwind · Motion · React Hook Form · Zod · Sonner ·
next-themes · Lucide · CVA · tailwind-merge. Icons are **Lucide** (no emoji).

**Deferred until a consumer exists** (we don't install unused machinery):
`TanStack Table` → lands with the candidate roster (Epic 3); `cmdk` → with a command
palette; **AI components** (`components/ai/*` — recommendation card, confidence badge,
evidence panel, with their own visual language) → with real AI output (Epic 5).

## Architecture
`UI → service (services/*) → typed DTO → apiClient → backend`. Components never call
`fetch()`. New reusable UI is added here and older pages are refactored onto it, so the
whole app trends toward one cohesive language.

## Accessibility & responsive
Keyboard-navigable, visible focus rings, ARIA labels on icon-only controls, semantic
headings. Desktop-first, but layouts are fluid (`sm:` breakpoints) and usable on mobile.

## AI intelligence surface (Story 5.4B)
The recruiter evaluation experience has its own restrained visual language under
`components/ai/` (see `components/ai/README.md`). Rules that keep it credible:
- **AI is marked, never loud** — a small `Sparkles` marker + "AI-assisted assessment", faint
  indigo tint / left accent. No glowing badges, no rainbow "AI" colors, no score dashboard.
- **Never a bare number.** Recommendations render as humane labels (enum → copy in
  `presentation.ts`); confidence renders as a **level** ("High/Moderate/Low evidence
  confidence"), never a percentage. The raw 0–1 value appears only inside an explanation.
- **Every claim is grounded** to inspectable source evidence via the citation → `EvidenceSheet`
  drawer. Tone is never carried by color alone (icon + label + text throughout).
- New primitives: `components/ui/sheet.tsx` (Radix-based side/bottom sheet; bottom on mobile,
  right panel on `sm+`) and a `destructive` `Badge` variant.

## Application shell & navigation (Story 6.1 → 7.1)
Story 6.1 kept a top nav; **Story 7.1 moved to a sidebar shell** now that the IA has real
depth (Dashboard · Review · Campaigns, with campaign → candidates → evaluation → history
beneath). The shell (`components/layout/`) is:
- **Desktop:** a `Sidebar` (collapsible to icons-only, persisted in `localStorage`) with the
  brand, the three real destinations (active state via `aria-current`), and account
  (org + email) + theme + logout anchored at the foot. Above the content, a slim
  **breadcrumb bar** appears on deep pages only.
- **Mobile:** a `MobileNav` top bar + a left slide-in drawer (Radix Dialog) with the same
  destinations + account; closes on navigation; reduced-motion safe.
- **Breadcrumbs** (`breadcrumbs.tsx`) are computed from the path; dynamic id segments are
  humanized by a page-supplied label (campaign role title, candidate name via
  `useBreadcrumbLabels`) or a positional fallback, so deep pages always say where you are
  and on which object. `nav-items.ts` is the single source of truth for destinations —
  only real ones; no invented Settings/Analytics/Reports.

**Story 7.2 — one shell, one nav model.** Recruiter routes live under the `app/(recruiter)/`
route group with a single `layout.tsx` (AppShell), so the shell + its identity (`/me`) fetch
+ sidebar state mount **once** across Dashboard/Campaigns/Review — not per-tree. `(auth)`
(login/signup) and `/invite` (candidate) stay separate trust/experience boundaries. URLs are
unchanged (route groups don't appear in the path). **Up-navigation is one model per
breakpoint:** desktop uses the breadcrumb bar; each deep page's per-page "Back to …" link is
`lg:hidden` (mobile-only, where breadcrumbs aren't shown) — never two controls for the same
action. **Return-to-work:** recording a human decision fires a success toast with a "Review
queue" action, so a recruiter who came from the queue is never stranded deep in a candidate
route.

## Review queue surface (Story 6.1)
The operational inbox at `/review-queue`. Compact filter chips carry whole-queue counts and
double as the summary (no giant KPI cards); one server-side name search; responsive item
**cards** (not a desktop-only table) so it's usable one-handed on mobile. Each card shows
who/role, a stage chip (icon + text, never color alone), recommendation + evidence
confidence when evaluated (reusing `components/ai/presentation.ts`), last activity, and
exactly one contextual action. Attention items get a subtle left accent; waiting/completed
are visually quiet. Backend pagination (Prev/Next). Stage vocabulary lives in
`components/review/queue-presentation.ts`; recommendation/confidence vocabulary is never
duplicated.

## First-run / activation (Story 7.3)
The workflow itself is the onboarding — no tour, no "skip onboarding" modal, no seeded fake
data. Comprehension comes from copy + hierarchy + contextual guidance on real system state:
- **Landing** states the thesis (evidence over résumé keywords) + a compact 4-step "how it
  works" + one dominant CTA into signup. No fabricated logos/stats/claims.
- **Empty dashboard** (zero campaigns) is a purposeful first-run state: the 4-step workflow +
  a single "Create your first campaign" action — never zero-filled analytics.
- **Draft → activate is sequenced:** a draft campaign's dominant action is "Design work
  sample"; **Activate is disabled until every competency is covered** (read from the existing
  work-sample API — guidance only; the backend remains the authority). This prevents the
  newcomer "click Activate → error" dead-end.
- **Work Sample Designer** opens with a one-line concept ("produce evidence, not trivia") and
  the coverage card explains why uncovered competencies block activation.
- Copy uses the product vocabulary throughout; no developer/domain leakage reaches the UI.

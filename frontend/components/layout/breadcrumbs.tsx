"use client";

import { ChevronRight } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

// Breadcrumbs give deep campaign/candidate/evaluation pages a sense of place. They are
// computed from the pathname; dynamic id segments are humanized either by a page-supplied
// label (e.g. the campaign's role title, the candidate's name) or a sensible positional
// fallback — so the trail reads well even on a cold deep-link.

type Labels = Record<string, string>;

const BreadcrumbContext = createContext<{ labels: Labels; register: (l: Labels) => void } | null>(
  null,
);

export function BreadcrumbProvider({ children }: { children: ReactNode }) {
  const [labels, setLabels] = useState<Labels>({});
  const register = useCallback(
    (l: Labels) => setLabels((prev) => ({ ...prev, ...l })),
    [],
  );
  const value = useMemo(() => ({ labels, register }), [labels, register]);
  return <BreadcrumbContext.Provider value={value}>{children}</BreadcrumbContext.Provider>;
}

/** A page registers human labels for the dynamic id segments it knows about, e.g.
 * `useBreadcrumbLabels({ [campaignId]: campaign.role_title })`. Safe no-op outside a shell. */
export function useBreadcrumbLabels(map: Labels): void {
  const ctx = useContext(BreadcrumbContext);
  const key = JSON.stringify(map);
  const register = ctx?.register;
  useEffect(() => {
    if (register && Object.keys(map).length > 0) register(map);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key, register]);
}

// Known static path segments → labels. Dynamic (id) segments fall through to a page label
// or a positional fallback based on the preceding segment.
const STATIC: Record<string, string> = {
  campaigns: "Campaigns",
  "review-queue": "Review queue",
  dashboard: "Dashboard",
  candidates: "Candidates",
  "work-sample": "Work sample",
  timeline: "History",
  new: "New campaign",
};

function fallback(previousSegment: string): string {
  if (previousSegment === "campaigns") return "Campaign";
  if (previousSegment === "candidates") return "Candidate";
  return "Details";
}

export function Breadcrumbs() {
  const pathname = usePathname();
  const ctx = useContext(BreadcrumbContext);
  const labels = ctx?.labels ?? {};

  const segments = pathname.split("/").filter(Boolean);
  if (segments.length <= 1) return null; // top-level pages don't need breadcrumbs

  const crumbs = segments.map((seg, i) => ({
    href: "/" + segments.slice(0, i + 1).join("/"),
    label: STATIC[seg] ?? labels[seg] ?? fallback(segments[i - 1] ?? ""),
    last: i === segments.length - 1,
  }));

  return (
    <nav aria-label="Breadcrumb" className="min-w-0">
      <ol className="flex items-center gap-1.5 text-sm">
        {crumbs.map((c, i) => (
          <li key={c.href} className="flex min-w-0 items-center gap-1.5">
            {i > 0 && (
              <ChevronRight className="text-muted-foreground/40 size-3.5 shrink-0" aria-hidden />
            )}
            {c.last ? (
              <span
                className="text-foreground max-w-[16rem] truncate font-medium"
                aria-current="page"
              >
                {c.label}
              </span>
            ) : (
              <Link
                href={c.href}
                className="text-muted-foreground hover:text-foreground max-w-[12rem] truncate transition-colors"
              >
                {c.label}
              </Link>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
}

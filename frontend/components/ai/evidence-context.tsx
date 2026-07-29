"use client";

import { createContext, useContext, useMemo, useState, type ReactNode } from "react";

import type { SubmittedEvidenceItem } from "@/types/evaluation";

import { EvidenceSheet } from "./evidence-sheet";

// Lets any nested citation open the source-evidence sheet without prop-drilling. The
// provider owns the evidence lookup (by evidence_id) + the open sheet state, and renders
// the sheet once at the boundary.
interface EvidenceContextValue {
  getByEvidenceId: (evidenceId: string) => SubmittedEvidenceItem | undefined;
  open: (evidenceId: string) => void;
  available: boolean;
}

const EvidenceContext = createContext<EvidenceContextValue | null>(null);

export function useEvidence(): EvidenceContextValue {
  const ctx = useContext(EvidenceContext);
  if (!ctx) throw new Error("useEvidence must be used within an EvidenceProvider");
  return ctx;
}

export function EvidenceProvider({
  items,
  children,
}: {
  items: SubmittedEvidenceItem[];
  children: ReactNode;
}) {
  const [activeId, setActiveId] = useState<string | null>(null);
  const byId = useMemo(
    () => new Map(items.map((item) => [item.evidence_id, item])),
    [items],
  );

  const value = useMemo<EvidenceContextValue>(
    () => ({
      getByEvidenceId: (id) => byId.get(id),
      open: setActiveId,
      available: items.length > 0,
    }),
    [byId, items.length],
  );

  const active = activeId ? (byId.get(activeId) ?? null) : null;

  return (
    <EvidenceContext.Provider value={value}>
      {children}
      <EvidenceSheet
        item={active}
        open={activeId !== null}
        onOpenChange={(o) => {
          if (!o) setActiveId(null);
        }}
      />
    </EvidenceContext.Provider>
  );
}

import { CheckCircle2, Download, X } from "lucide-react";

import { Button } from "@/components/ui/button";
import type { CandidateImportSummary } from "@/types/candidate";

// Shown after a CSV import — a persistent, dismissible summary (not just a toast) so
// the recruiter can read what happened. The issue-report download is designed-in but
// disabled until it's generated server-side (roadmap).
export function ImportResultsPanel({
  summary,
  onDismiss,
}: {
  summary: CandidateImportSummary;
  onDismiss: () => void;
}) {
  return (
    <div className="bg-card animate-fade-in rounded-xl border p-4 shadow-subtle">
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-center gap-2">
          <CheckCircle2 className="text-success size-5" aria-hidden />
          <p className="font-medium">Import complete</p>
        </div>
        <button
          onClick={onDismiss}
          aria-label="Dismiss"
          className="text-muted-foreground hover:text-foreground"
        >
          <X className="size-4" />
        </button>
      </div>

      <div className="mt-3 flex flex-wrap gap-x-6 gap-y-1 text-sm">
        <span>
          <strong className="tabular-nums">{summary.imported}</strong> imported
        </span>
        <span className="text-muted-foreground">
          <strong className="tabular-nums">{summary.skipped}</strong> skipped
        </span>
        <span className={summary.failed > 0 ? "text-destructive" : "text-muted-foreground"}>
          <strong className="tabular-nums">{summary.failed}</strong> failed
        </span>
      </div>

      {summary.issues.length > 0 && (
        <ul className="text-muted-foreground mt-3 max-h-40 space-y-1 overflow-y-auto text-xs">
          {summary.issues.map((issue, i) => (
            <li key={i}>
              Row {issue.row}: {issue.reason}
              {issue.email ? ` (${issue.email})` : ""}
            </li>
          ))}
        </ul>
      )}

      <div className="mt-4">
        <Button variant="outline" size="sm" disabled title="Coming soon">
          <Download className="size-4" aria-hidden />
          Download issue report
        </Button>
      </div>
    </div>
  );
}

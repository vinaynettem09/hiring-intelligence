"use client";

import { FileText } from "lucide-react";

import {
  Sheet,
  SheetBody,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import type { SubmittedEvidenceItem } from "@/types/evaluation";

// The source behind a citation: the candidate's verbatim submitted response, with the
// task that prompted it. This is the recruiter's authorized view of the real evidence —
// the trust anchor that makes an assessment inspectable rather than a black box.
export function EvidenceSheet({
  item,
  open,
  onOpenChange,
}: {
  item: SubmittedEvidenceItem | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}) {
  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent>
        <SheetHeader>
          <SheetTitle className="flex items-center gap-2">
            <FileText className="text-muted-foreground size-4" aria-hidden />
            {item ? `Task ${item.task_number}` : "Evidence"}
          </SheetTitle>
          <SheetDescription>
            The submitted work-sample evidence behind this assessment.
          </SheetDescription>
        </SheetHeader>
        <SheetBody>
          {item ? (
            <div className="space-y-6">
              <section className="space-y-1.5">
                <h4 className="text-muted-foreground text-xs font-medium uppercase tracking-wide">
                  Task prompt
                </h4>
                <p className="text-sm">{item.task_prompt}</p>
              </section>
              <section className="space-y-1.5">
                <h4 className="text-muted-foreground text-xs font-medium uppercase tracking-wide">
                  What this task looks for
                </h4>
                <p className="text-muted-foreground text-sm">{item.evidence_intent}</p>
              </section>
              <section className="space-y-1.5">
                <h4 className="text-muted-foreground text-xs font-medium uppercase tracking-wide">
                  Candidate&rsquo;s submitted response
                </h4>
                <div className="bg-muted/40 rounded-lg border p-4 text-sm leading-relaxed whitespace-pre-wrap">
                  {item.response_text || (
                    <span className="text-muted-foreground italic">No response was submitted.</span>
                  )}
                </div>
              </section>
            </div>
          ) : (
            <p className="text-muted-foreground text-sm">
              The source evidence for this citation isn&rsquo;t available to display.
            </p>
          )}
        </SheetBody>
      </SheetContent>
    </Sheet>
  );
}

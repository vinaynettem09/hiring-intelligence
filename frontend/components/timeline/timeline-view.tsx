"use client";

import {
  Download,
  FileCheck2,
  Gavel,
  Mail,
  MailOpen,
  ShieldCheck,
  ShieldX,
  Sparkles,
  type LucideIcon,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import type { HiringTimelineResponse, TimelineEntry, TimelineEventKind } from "@/types/timeline";

const KIND: Record<TimelineEventKind, { Icon: LucideIcon; tint: string }> = {
  INVITATION_SENT: { Icon: Mail, tint: "text-muted-foreground" },
  INVITATION_OPENED: { Icon: MailOpen, tint: "text-muted-foreground" },
  CONSENT_GRANTED: { Icon: ShieldCheck, tint: "text-success" },
  CONSENT_WITHDRAWN: { Icon: ShieldX, tint: "text-destructive" },
  WORK_SAMPLE_SUBMITTED: { Icon: FileCheck2, tint: "text-primary" },
  EVALUATION_GENERATED: { Icon: Sparkles, tint: "text-primary" },
  DECISION_RECORDED: { Icon: Gavel, tint: "text-foreground" },
};

const ACTOR_LABEL: Record<string, string> = {
  recruiter: "Recruiter",
  candidate: "Candidate",
  system: "System",
};

function toCsv(timeline: HiringTimelineResponse): string {
  const esc = (v: string) => `"${v.replace(/"/g, '""')}"`;
  const header = ["timestamp", "event", "actor_type", "actor", "summary"];
  const rows = timeline.entries.map((e) =>
    [e.at, e.kind, e.actor_type, e.actor ?? "", e.summary].map((v) => esc(String(v))).join(","),
  );
  return [header.join(","), ...rows].join("\r\n");
}

function download(timeline: HiringTimelineResponse): void {
  const blob = new Blob([toCsv(timeline)], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `hiring-timeline-${timeline.candidate_evaluation_id}.csv`;
  a.click();
  URL.revokeObjectURL(url);
}

export function TimelineView({ timeline }: { timeline: HiringTimelineResponse }) {
  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between gap-3">
        <p className="text-muted-foreground text-sm">
          {timeline.entries.length} recorded {timeline.entries.length === 1 ? "event" : "events"},
          oldest first.
        </p>
        <Button
          variant="outline"
          size="sm"
          onClick={() => download(timeline)}
          disabled={timeline.entries.length === 0}
        >
          <Download className="size-4" aria-hidden />
          Export CSV
        </Button>
      </div>

      {timeline.entries.length === 0 ? (
        <p className="text-muted-foreground text-sm">No recorded events yet.</p>
      ) : (
        <ol className="relative space-y-4 border-l pl-6">
          {timeline.entries.map((entry, i) => (
            <TimelineRow key={i} entry={entry} />
          ))}
        </ol>
      )}
    </div>
  );
}

function TimelineRow({ entry }: { entry: TimelineEntry }) {
  const { Icon, tint } = KIND[entry.kind];
  const actor = entry.actor ?? ACTOR_LABEL[entry.actor_type] ?? entry.actor_type;
  return (
    <li className="relative">
      <span
        className={cn(
          "bg-background absolute -left-[33px] flex size-6 items-center justify-center rounded-full border",
        )}
      >
        <Icon className={cn("size-3.5", tint)} aria-hidden />
      </span>
      <p className="text-sm">{entry.summary}</p>
      <p className="text-muted-foreground mt-0.5 text-xs">
        {actor} · {new Date(entry.at).toLocaleString()}
      </p>
    </li>
  );
}

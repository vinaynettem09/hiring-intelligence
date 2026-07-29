"use client";

import {
  type ColumnDef,
  type SortingState,
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table";
import {
  ArrowDown,
  ArrowUp,
  ChevronsUpDown,
  Eye,
  FileText,
  Minus,
  Send,
  Sparkles,
} from "lucide-react";
import Link from "next/link";
import { useMemo, useState } from "react";

import { recommendationPresentation, recommendationShortLabel } from "@/components/ai/presentation";
import { Badge, type BadgeProps } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import type { Recommendation } from "@/types/evaluation";
import type { RosterEntry } from "@/types/candidate";

const TONE_TO_BADGE: Record<string, BadgeProps["variant"]> = {
  positive: "success",
  moderate: "warning",
  negative: "destructive",
  review: "primary",
};

function EvaluationCell({ row }: { row: RosterEntry }) {
  if (row.has_evaluation && row.latest_recommendation) {
    const rec = row.latest_recommendation as Recommendation;
    const { tone } = recommendationPresentation(rec);
    return (
      <span className="inline-flex items-center gap-1.5">
        <Badge variant={TONE_TO_BADGE[tone]} className="normal-case">
          {recommendationShortLabel(rec)}
        </Badge>
        {row.latest_run_number != null && row.latest_run_number > 1 && (
          <span className="text-muted-foreground text-xs tabular-nums">
            run {row.latest_run_number}
          </span>
        )}
      </span>
    );
  }
  if (row.status === "submitted") {
    return <span className="text-muted-foreground text-xs">Not evaluated</span>;
  }
  return <span className="text-muted-foreground/40 text-xs">&mdash;</span>;
}

const BASE_COLUMNS: ColumnDef<RosterEntry>[] = [
  {
    id: "name",
    accessorFn: (row) => row.candidate.name,
    header: "Name",
    cell: (info) => <span className="font-medium">{info.getValue<string>()}</span>,
  },
  {
    id: "email",
    accessorFn: (row) => row.candidate.email,
    header: "Email",
    enableSorting: false,
    cell: (info) => <span className="text-muted-foreground">{info.getValue<string>()}</span>,
  },
  {
    accessorKey: "status",
    header: "Status",
    enableSorting: false,
    cell: (info) => <Badge variant="neutral">{info.getValue<string>()}</Badge>,
  },
  {
    id: "evaluation",
    header: "Evaluation",
    enableSorting: false,
    cell: ({ row }) => <EvaluationCell row={row.original} />,
  },
  {
    accessorKey: "has_resume",
    header: "Résumé",
    enableSorting: false,
    cell: (info) =>
      info.getValue<boolean>() ? (
        <FileText className="text-muted-foreground size-4" aria-label="Résumé attached" />
      ) : (
        <Minus className="text-muted-foreground/40 size-4" aria-label="No résumé" />
      ),
  },
  {
    id: "added",
    accessorKey: "created_at",
    header: "Added",
    cell: (info) => (
      <span className="text-muted-foreground tabular-nums">
        {new Date(info.getValue<string>()).toLocaleDateString()}
      </span>
    ),
  },
];

export function RosterTable({
  data,
  campaignId,
  onInvite,
  invitingId,
  onGenerate,
  generatingId,
}: {
  data: RosterEntry[];
  campaignId: string;
  onInvite?: (evaluationId: string) => void;
  invitingId?: string | null;
  onGenerate?: (evaluationId: string) => void;
  generatingId?: string | null;
}) {
  const [sorting, setSorting] = useState<SortingState>([]);

  // Exactly ONE contextual action per row — never a cluster of AI buttons.
  const columns = useMemo<ColumnDef<RosterEntry>[]>(
    () => [
      ...BASE_COLUMNS,
      {
        id: "actions",
        header: "",
        enableSorting: false,
        cell: ({ row }) => {
          const entry = row.original;
          const id = entry.evaluation_id;
          if (entry.has_evaluation) {
            return (
              <div className="text-right">
                <Link href={`/campaigns/${campaignId}/candidates/${id}`}>
                  <Button variant="outline" size="sm">
                    <Eye className="size-3.5" aria-hidden />
                    View evaluation
                  </Button>
                </Link>
              </div>
            );
          }
          if (entry.status === "submitted" && onGenerate) {
            return (
              <div className="text-right">
                <Button
                  variant="outline"
                  size="sm"
                  loading={generatingId === id}
                  onClick={() => onGenerate(id)}
                >
                  <Sparkles className="size-3.5" aria-hidden />
                  Generate evaluation
                </Button>
              </div>
            );
          }
          if (onInvite) {
            return (
              <div className="text-right">
                <Button
                  variant="ghost"
                  size="sm"
                  loading={invitingId === id}
                  onClick={() => onInvite(id)}
                >
                  <Send className="size-3.5" aria-hidden />
                  Invite
                </Button>
              </div>
            );
          }
          return null;
        },
      },
    ],
    [campaignId, onInvite, invitingId, onGenerate, generatingId],
  );

  const table = useReactTable({
    data,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  return (
    <div className="overflow-x-auto rounded-xl border">
      <table className="w-full text-sm">
        <thead className="bg-muted/50 sticky top-0 z-10">
          {table.getHeaderGroups().map((group) => (
            <tr key={group.id}>
              {group.headers.map((header) => {
                const sorted = header.column.getIsSorted();
                return (
                  <th key={header.id} className="px-4 py-2.5 text-left font-medium">
                    {header.column.getCanSort() ? (
                      <button
                        type="button"
                        onClick={header.column.getToggleSortingHandler()}
                        className="hover:text-foreground inline-flex items-center gap-1"
                      >
                        {flexRender(header.column.columnDef.header, header.getContext())}
                        {sorted === "asc" ? (
                          <ArrowUp className="size-3.5" />
                        ) : sorted === "desc" ? (
                          <ArrowDown className="size-3.5" />
                        ) : (
                          <ChevronsUpDown className="text-muted-foreground/50 size-3.5" />
                        )}
                      </button>
                    ) : (
                      flexRender(header.column.columnDef.header, header.getContext())
                    )}
                  </th>
                );
              })}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => (
            <tr key={row.id} className="hover:bg-muted/30 border-t transition-colors">
              {row.getVisibleCells().map((cell) => (
                <td key={cell.id} className="px-4 py-3">
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

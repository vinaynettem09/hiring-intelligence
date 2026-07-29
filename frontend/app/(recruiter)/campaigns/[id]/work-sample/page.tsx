"use client";

import {
  ArrowDown,
  ArrowLeft,
  ArrowUp,
  CheckCircle2,
  ChevronDown,
  Eye,
  Pencil,
  Plus,
  Trash2,
  TriangleAlert,
} from "lucide-react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useCallback, useEffect, useMemo, useState } from "react";
import { toast } from "sonner";

import { ErrorState } from "@/components/feedback/error-state";
import { FadeIn } from "@/components/motion/motion";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { Textarea } from "@/components/ui/textarea";
import { ApiError } from "@/lib/api-client";
import { authStore } from "@/lib/auth-store";
import { cn } from "@/lib/utils";
import { CampaignService } from "@/services/campaign-service";
import { WorkSampleService } from "@/services/work-sample-service";
import type { WorkSample } from "@/types/work-sample";

interface EditTask {
  key: string;
  prompt: string;
  evidence_intent: string;
  competencies: string[];
  instructions: string;
  effort: string;
  expanded: boolean;
}

function fromServer(ws: WorkSample): EditTask[] {
  return ws.tasks.map((t, i) => ({
    key: `srv-${i}`,
    prompt: t.prompt,
    evidence_intent: t.evidence_intent,
    competencies: t.competencies,
    instructions: t.instructions ?? "",
    effort: t.expected_effort_minutes != null ? String(t.expected_effort_minutes) : "",
    expanded: false,
  }));
}

export default function WorkSampleDesignerPage() {
  const router = useRouter();
  const { id } = useParams<{ id: string }>();

  const [competencyNames, setCompetencyNames] = useState<string[]>([]);
  const [editable, setEditable] = useState(true);
  const [roleTitle, setRoleTitle] = useState("");
  const [title, setTitle] = useState("");
  const [introduction, setIntroduction] = useState("");
  const [tasks, setTasks] = useState<EditTask[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<{ message: string; correlationId: string | null } | null>(null);
  const [saving, setSaving] = useState(false);
  const [preview, setPreview] = useState(false);
  const [nextKey, setNextKey] = useState(0);

  const load = useCallback(() => {
    setLoading(true);
    setError(null);
    Promise.all([CampaignService.get(id), WorkSampleService.get(id)])
      .then(([campaignRes, wsRes]) => {
        setCompetencyNames(campaignRes.data.role_profile.competencies.map((c) => c.name));
        const ws = wsRes.data;
        setEditable(ws.editable);
        setRoleTitle(ws.role_title);
        setTitle(ws.title || "Structured work sample");
        setIntroduction(ws.introduction ?? "");
        setTasks(fromServer(ws));
      })
      .catch((e: unknown) => {
        if (e instanceof ApiError && e.status === 401) {
          router.replace("/login");
          return;
        }
        setError({
          message: e instanceof Error ? e.message : "Failed to load the work sample",
          correlationId: e instanceof ApiError ? e.body.correlation_id : null,
        });
      })
      .finally(() => setLoading(false));
  }, [id, router]);

  useEffect(() => {
    if (!authStore.getAccess()) {
      router.replace("/login");
      return;
    }
    load();
  }, [load, router]);

  const coverage = useMemo(() => {
    const measured = new Set(tasks.flatMap((t) => t.competencies));
    return {
      covered: competencyNames.filter((n) => measured.has(n)),
      uncovered: competencyNames.filter((n) => !measured.has(n)),
    };
  }, [tasks, competencyNames]);

  const estimatedMinutes = tasks.reduce((sum, t) => sum + (Number(t.effort) || 0), 0);

  const taskValid = (t: EditTask) =>
    t.prompt.trim() && t.evidence_intent.trim() && t.competencies.length > 0;
  const canSave = title.trim().length > 0 && tasks.every(taskValid);

  function patch(key: string, changes: Partial<EditTask>) {
    setTasks((prev) => prev.map((t) => (t.key === key ? { ...t, ...changes } : t)));
  }
  function addTask() {
    setTasks((prev) => [
      ...prev,
      {
        key: `new-${nextKey}`,
        prompt: "",
        evidence_intent: "",
        competencies: [],
        instructions: "",
        effort: "",
        expanded: true,
      },
    ]);
    setNextKey((k) => k + 1);
  }
  function removeTask(key: string) {
    setTasks((prev) => prev.filter((t) => t.key !== key));
  }
  function move(key: string, dir: -1 | 1) {
    setTasks((prev) => {
      const i = prev.findIndex((t) => t.key === key);
      const j = i + dir;
      if (i < 0 || j < 0 || j >= prev.length) return prev;
      const next = [...prev];
      [next[i], next[j]] = [next[j], next[i]];
      return next;
    });
  }
  function toggleCompetency(key: string, name: string) {
    setTasks((prev) =>
      prev.map((t) =>
        t.key === key
          ? {
              ...t,
              competencies: t.competencies.includes(name)
                ? t.competencies.filter((c) => c !== name)
                : [...t.competencies, name],
            }
          : t,
      ),
    );
  }

  async function onSave() {
    setSaving(true);
    try {
      const res = await WorkSampleService.define(id, {
        title: title.trim(),
        introduction: introduction.trim() || null,
        tasks: tasks.map((t) => ({
          prompt: t.prompt.trim(),
          evidence_intent: t.evidence_intent.trim(),
          competencies: t.competencies,
          instructions: t.instructions.trim() || null,
          expected_effort_minutes: t.effort ? Number(t.effort) : null,
        })),
      });
      setTasks(fromServer(res.data));
      toast.success("Work sample saved");
    } catch (e: unknown) {
      if (e instanceof ApiError && e.status === 401) {
        router.replace("/login");
        return;
      }
      toast.error(e instanceof Error ? e.message : "Could not save the work sample");
    } finally {
      setSaving(false);
    }
  }

  const back = (
    <Link
      href={`/campaigns/${id}`}
      className="text-muted-foreground hover:text-foreground inline-flex items-center gap-1 text-sm transition-colors lg:hidden"
    >
      <ArrowLeft className="size-4" aria-hidden />
      Back to campaign
    </Link>
  );

  if (loading) {
    return (
      <div className="space-y-6">
        {back}
        <Skeleton className="h-8 w-72" />
        <Skeleton className="h-24 w-full rounded-xl" />
        <Skeleton className="h-64 w-full rounded-xl" />
      </div>
    );
  }
  if (error) {
    return (
      <div className="space-y-6">
        {back}
        <ErrorState
          message={error.message}
          correlationId={error.correlationId}
          action={
            <Button variant="outline" size="sm" onClick={load}>
              Try again
            </Button>
          }
        />
      </div>
    );
  }

  return (
    <FadeIn className="space-y-6">
      {back}

      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div className="space-y-1">
          <p className="text-muted-foreground text-sm">{roleTitle}</p>
          <h1 className="text-2xl font-semibold tracking-tight">Structured work sample</h1>
          <p className="text-muted-foreground text-sm">
            {tasks.length} {tasks.length === 1 ? "task" : "tasks"} · ~{estimatedMinutes} min ·{" "}
            {coverage.covered.length}/{competencyNames.length} competencies covered
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" onClick={() => setPreview((p) => !p)}>
            {preview ? <Pencil className="size-4" /> : <Eye className="size-4" />}
            {preview ? "Edit" : "Preview as candidate"}
          </Button>
          {editable && !preview && (
            <Button onClick={onSave} loading={saving} disabled={!canSave}>
              Save work sample
            </Button>
          )}
        </div>
      </div>

      {!editable && (
        <div className="border-warning/30 bg-warning/10 text-warning flex items-center gap-2 rounded-lg border px-4 py-2 text-sm">
          <TriangleAlert className="size-4 shrink-0" aria-hidden />
          This campaign is active — the work sample is frozen and can no longer be edited.
        </div>
      )}

      {preview ? (
        <CandidatePreview title={title} introduction={introduction} tasks={tasks} />
      ) : (
        <>
          {editable && (
            <div className="text-muted-foreground bg-muted/40 rounded-lg border px-4 py-3 text-sm leading-relaxed">
              Design tasks that give candidates a chance to{" "}
              <span className="text-foreground font-medium">produce evidence</span> for each
              competency — real work, not trivia. The AI only assesses what the submitted work
              actually shows.
            </div>
          )}
          <CoverageCard covered={coverage.covered} uncovered={coverage.uncovered} />

          {editable && (
            <Card>
              <CardContent className="space-y-4 pt-6">
                <label className="block space-y-1.5">
                  <span className="text-sm font-medium">Title</span>
                  <Input value={title} onChange={(e) => setTitle(e.target.value)} />
                </label>
                <label className="block space-y-1.5">
                  <span className="text-sm font-medium">Introduction (optional)</span>
                  <Textarea
                    value={introduction}
                    onChange={(e) => setIntroduction(e.target.value)}
                    placeholder="A short, welcoming intro shown to the candidate before they begin."
                  />
                </label>
              </CardContent>
            </Card>
          )}

          {tasks.length === 0 ? (
            <div className="rounded-xl border border-dashed px-6 py-12 text-center">
              <p className="font-medium">No tasks yet</p>
              <p className="text-muted-foreground mt-1 text-sm">
                Add a task for each thing you want candidates to demonstrate.
              </p>
              {editable && (
                <Button className="mt-4" onClick={addTask}>
                  <Plus className="size-4" aria-hidden />
                  Add first task
                </Button>
              )}
            </div>
          ) : (
            <div className="space-y-4">
              {tasks.map((task, index) => (
                <TaskCard
                  key={task.key}
                  index={index}
                  total={tasks.length}
                  task={task}
                  competencyOptions={competencyNames}
                  editable={editable}
                  onChange={(c) => patch(task.key, c)}
                  onToggleCompetency={(name) => toggleCompetency(task.key, name)}
                  onRemove={() => removeTask(task.key)}
                  onMove={(dir) => move(task.key, dir)}
                />
              ))}
              {editable && (
                <Button variant="outline" onClick={addTask} className="w-full">
                  <Plus className="size-4" aria-hidden />
                  Add task
                </Button>
              )}
            </div>
          )}
        </>
      )}
    </FadeIn>
  );
}

function CoverageCard({ covered, uncovered }: { covered: string[]; uncovered: string[] }) {
  const all = [...covered.map((n) => ({ n, ok: true })), ...uncovered.map((n) => ({ n, ok: false }))];
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">Competency coverage</CardTitle>
        <CardDescription>
          Every competency needs at least one task before the campaign can be activated — so
          each is backed by real evidence.
        </CardDescription>
      </CardHeader>
      <CardContent>
        {all.length === 0 ? (
          <p className="text-muted-foreground text-sm">This campaign has no competencies.</p>
        ) : (
          <ul className="space-y-2">
            {all.map((c) => (
              <li key={c.n} className="flex items-center gap-2 text-sm">
                {c.ok ? (
                  <CheckCircle2 className="text-success size-4 shrink-0" aria-hidden />
                ) : (
                  <TriangleAlert className="text-warning size-4 shrink-0" aria-hidden />
                )}
                <span className={cn("font-medium", !c.ok && "text-warning")}>{c.n}</span>
                {!c.ok && <span className="text-muted-foreground text-xs">· no task yet</span>}
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}

function TaskCard({
  index,
  total,
  task,
  competencyOptions,
  editable,
  onChange,
  onToggleCompetency,
  onRemove,
  onMove,
}: {
  index: number;
  total: number;
  task: EditTask;
  competencyOptions: string[];
  editable: boolean;
  onChange: (changes: Partial<EditTask>) => void;
  onToggleCompetency: (name: string) => void;
  onRemove: () => void;
  onMove: (dir: -1 | 1) => void;
}) {
  return (
    <Card>
      <CardContent className="space-y-4 pt-6">
        <div className="flex items-center justify-between">
          <span className="text-muted-foreground text-xs font-medium tracking-wide uppercase">
            Task {index + 1}
          </span>
          {editable && (
            <div className="flex items-center gap-1">
              <Button
                variant="ghost"
                size="icon"
                aria-label="Move up"
                disabled={index === 0}
                onClick={() => onMove(-1)}
              >
                <ArrowUp className="size-4" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                aria-label="Move down"
                disabled={index === total - 1}
                onClick={() => onMove(1)}
              >
                <ArrowDown className="size-4" />
              </Button>
              <Button variant="ghost" size="icon" aria-label="Remove task" onClick={onRemove}>
                <Trash2 className="size-4" />
              </Button>
            </div>
          )}
        </div>

        <label className="block space-y-1.5">
          <span className="text-sm font-medium">Candidate prompt</span>
          <Textarea
            value={task.prompt}
            disabled={!editable}
            onChange={(e) => onChange({ prompt: e.target.value })}
            placeholder="e.g. A service is producing intermittent duplicate payments. Explain how you'd investigate and mitigate it."
          />
        </label>

        <label className="block space-y-1.5">
          <span className="text-sm font-medium">Evidence we&apos;re trying to elicit</span>
          <Textarea
            value={task.evidence_intent}
            disabled={!editable}
            onChange={(e) => onChange({ evidence_intent: e.target.value })}
            placeholder="e.g. Structured incident reasoning, hypothesis formation, safe remediation."
          />
          <span className="text-muted-foreground text-xs">
            Recruiter-only — candidates never see this.
          </span>
        </label>

        <div className="space-y-1.5">
          <span className="text-sm font-medium">Measures</span>
          <div className="flex flex-wrap gap-2">
            {competencyOptions.map((name) => {
              const on = task.competencies.includes(name);
              return (
                <button
                  key={name}
                  type="button"
                  disabled={!editable}
                  onClick={() => onToggleCompetency(name)}
                  className={cn(
                    "rounded-full border px-2.5 py-0.5 text-xs font-medium transition-colors disabled:opacity-60",
                    on
                      ? "border-primary bg-primary/10 text-primary"
                      : "text-muted-foreground hover:text-foreground",
                  )}
                >
                  {name}
                </button>
              );
            })}
          </div>
          {task.competencies.length === 0 && (
            <span className="text-warning text-xs">Select at least one competency.</span>
          )}
        </div>

        {task.expanded ? (
          <div className="space-y-4 border-t pt-4">
            <label className="block space-y-1.5">
              <span className="text-sm font-medium">Instructions (optional)</span>
              <Textarea
                value={task.instructions}
                disabled={!editable}
                onChange={(e) => onChange({ instructions: e.target.value })}
              />
            </label>
            <label className="block space-y-1.5">
              <span className="text-sm font-medium">Estimated effort (minutes, optional)</span>
              <Input
                type="number"
                min={1}
                value={task.effort}
                disabled={!editable}
                onChange={(e) => onChange({ effort: e.target.value })}
                className="w-32"
              />
            </label>
          </div>
        ) : (
          <button
            type="button"
            onClick={() => onChange({ expanded: true })}
            className="text-muted-foreground hover:text-foreground inline-flex items-center gap-1 text-xs font-medium"
          >
            <ChevronDown className="size-3.5" aria-hidden />
            More options
          </button>
        )}
      </CardContent>
    </Card>
  );
}

// Read-only, candidate-facing view — the same information a candidate will see (no
// evidence intent, no competency mapping). Shares the calm presentation Story 4.4 builds on.
function CandidatePreview({
  title,
  introduction,
  tasks,
}: {
  title: string;
  introduction: string;
  tasks: EditTask[];
}) {
  return (
    <Card>
      <CardContent className="space-y-6 pt-6">
        <div className="space-y-1">
          <h2 className="text-lg font-semibold">{title}</h2>
          {introduction && <p className="text-muted-foreground text-sm">{introduction}</p>}
        </div>
        {tasks.map((task, i) => (
          <div key={task.key} className="space-y-2 border-t pt-4">
            <div className="flex items-center justify-between">
              <span className="text-muted-foreground text-xs font-medium tracking-wide uppercase">
                Task {i + 1}
              </span>
              {task.effort && (
                <span className="text-muted-foreground text-xs">~{task.effort} min</span>
              )}
            </div>
            <p className="text-sm whitespace-pre-wrap">{task.prompt || "—"}</p>
            {task.instructions && (
              <p className="text-muted-foreground text-sm whitespace-pre-wrap">
                {task.instructions}
              </p>
            )}
          </div>
        ))}
      </CardContent>
    </Card>
  );
}

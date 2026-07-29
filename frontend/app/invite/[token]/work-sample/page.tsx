"use client";

import { ArrowLeft, ArrowRight, Check, CircleAlert, CircleCheck, Loader2 } from "lucide-react";
import { useParams, useRouter } from "next/navigation";
import { useCallback, useEffect, useRef, useState } from "react";
import { toast } from "sonner";

import { CandidateProblem, problemForCode } from "@/components/candidate/candidate-problem";
import { CandidateShell } from "@/components/layout/candidate-shell";
import { FadeIn } from "@/components/motion/motion";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Skeleton } from "@/components/ui/skeleton";
import { Textarea } from "@/components/ui/textarea";
import { ApiError } from "@/lib/api-client";
import { CandidateWorkSampleService } from "@/services/candidate-work-sample-service";
import type { CandidateWorkSample } from "@/types/candidate-work-sample";

type SaveState = "saved" | "unsaved" | "saving" | "error";
type Screen = { kind: "loading" } | { kind: "ready" } | { kind: "problem"; code: string | null };
interface Completion {
  organization_name: string;
  role_title: string;
  submitted_at: string;
}

const answered = (text: string) => text.trim().length > 0;

export default function CandidateWorkSamplePage() {
  const { token } = useParams<{ token: string }>();
  const router = useRouter();

  const [screen, setScreen] = useState<Screen>({ kind: "loading" });
  const [ws, setWs] = useState<CandidateWorkSample | null>(null);
  const [responses, setResponses] = useState<Record<string, string>>({});
  const [index, setIndex] = useState(0);
  const [reviewing, setReviewing] = useState(false);
  const [saveState, setSaveState] = useState<SaveState>("saved");
  const [completion, setCompletion] = useState<Completion | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const pending = useRef<{ taskId: string; text: string } | null>(null);

  const load = useCallback(() => {
    setScreen({ kind: "loading" });
    CandidateWorkSampleService.load(token)
      .then((res) => {
        setWs(res.data);
        setResponses(Object.fromEntries(res.data.tasks.map((t) => [t.task_id, t.response_text])));
        if (res.data.submitted && res.data.submitted_at) {
          setCompletion({
            organization_name: res.data.organization_name,
            role_title: res.data.role_title,
            submitted_at: res.data.submitted_at,
          });
        }
        setScreen({ kind: "ready" });
      })
      .catch((e: unknown) => {
        const code = e instanceof ApiError ? e.body.code : null;
        if (code === "CONSENT_REQUIRED") {
          router.replace(`/invite/${token}/consent`);
          return;
        }
        setScreen({ kind: "problem", code });
      });
  }, [token, router]);

  useEffect(() => {
    load();
  }, [load]);

  const doSave = useCallback(
    async (taskId: string, text: string) => {
      pending.current = null;
      setSaveState("saving");
      try {
        await CandidateWorkSampleService.saveResponse(token, taskId, text);
        setSaveState("saved");
      } catch (e: unknown) {
        const code = e instanceof ApiError ? e.body.code : null;
        if (code === "CONSENT_REQUIRED") {
          router.replace(`/invite/${token}/consent`);
          return;
        }
        if (code && code.startsWith("INVITATION_")) {
          setScreen({ kind: "problem", code });
          return;
        }
        setSaveState("error");
      }
    },
    [token, router],
  );

  function onType(taskId: string, text: string) {
    setResponses((prev) => ({ ...prev, [taskId]: text }));
    setSaveState("unsaved");
    pending.current = { taskId, text };
    if (timer.current) clearTimeout(timer.current);
    timer.current = setTimeout(() => {
      if (pending.current) void doSave(pending.current.taskId, pending.current.text);
    }, 900);
  }

  const flush = useCallback(async () => {
    if (timer.current) clearTimeout(timer.current);
    if (pending.current) await doSave(pending.current.taskId, pending.current.text);
  }, [doSave]);

  async function go(to: number | "review") {
    await flush();
    if (to === "review") setReviewing(true);
    else {
      setReviewing(false);
      setIndex(to);
    }
  }

  async function onSubmit() {
    setSubmitting(true);
    try {
      await flush(); // never submit a stale server draft — land the last autosave first
      const res = await CandidateWorkSampleService.submit(token);
      setCompletion({
        organization_name: res.data.organization_name,
        role_title: res.data.role_title,
        submitted_at: res.data.submitted_at,
      });
    } catch (e: unknown) {
      const code = e instanceof ApiError ? e.body.code : null;
      if (code === "CONSENT_REQUIRED") {
        router.replace(`/invite/${token}/consent`);
        return;
      }
      if (code && code.startsWith("INVITATION_")) {
        setScreen({ kind: "problem", code });
        return;
      }
      if (code === "WORK_SAMPLE_ALREADY_SUBMITTED") {
        load(); // it was already submitted — reload into the completion state
        return;
      }
      if (code === "WORK_SAMPLE_INCOMPLETE") {
        toast.error("Please answer every task before submitting.");
        return;
      }
      if (e instanceof ApiError) {
        toast.error(e.message);
        return;
      }
      // Genuine network ambiguity — we don't know if it committed. Don't claim failure.
      toast.message("We couldn’t confirm whether your work was submitted — checking…");
      load();
    } finally {
      setSubmitting(false);
    }
  }

  if (screen.kind === "loading") {
    return (
      <CandidateShell>
        <div className="space-y-4">
          <Skeleton className="h-6 w-1/2" />
          <Skeleton className="h-2 w-full rounded-full" />
          <Skeleton className="h-64 w-full rounded-xl" />
        </div>
      </CandidateShell>
    );
  }
  if (screen.kind === "problem") {
    return (
      <CandidateShell>
        <CandidateProblem
          {...problemForCode(screen.code)}
          action={
            screen.code === null ? (
              <Button variant="outline" onClick={load}>
                Try again
              </Button>
            ) : undefined
          }
        />
      </CandidateShell>
    );
  }
  if (!ws) return null;

  if (completion) {
    return (
      <CandidateShell>
        <CompletionScreen completion={completion} />
      </CandidateShell>
    );
  }

  const total = ws.tasks.length;
  const answeredCount = ws.tasks.filter((t) => answered(responses[t.task_id] ?? "")).length;

  return (
    <CandidateShell>
      <div className="space-y-6">
        <div className="space-y-2">
          <p className="text-muted-foreground text-sm">
            {ws.organization_name} · {ws.role_title}
          </p>
          <div className="flex items-center justify-between gap-4">
            <h1 className="text-xl font-semibold tracking-tight">{ws.title}</h1>
            <span className="text-muted-foreground shrink-0 text-sm">
              {reviewing ? "Review" : `Task ${index + 1} of ${total}`}
            </span>
          </div>
          <div className="bg-secondary h-1.5 w-full overflow-hidden rounded-full">
            <div
              className="bg-primary h-full rounded-full transition-all"
              style={{ width: `${total ? (answeredCount / total) * 100 : 0}%` }}
              role="progressbar"
              aria-valuenow={answeredCount}
              aria-valuemin={0}
              aria-valuemax={total}
              aria-label="Tasks answered"
            />
          </div>
          <p className="text-muted-foreground text-xs">
            {answeredCount} of {total} answered · ~{ws.estimated_minutes} min total
          </p>
        </div>

        {reviewing ? (
          <ReviewScreen
            ws={ws}
            responses={responses}
            submitting={submitting}
            onEdit={(i) => go(i)}
            onSubmit={onSubmit}
          />
        ) : (
          <TaskScreen
            key={ws.tasks[index].task_id}
            prompt={ws.tasks[index].prompt}
            instructions={ws.tasks[index].instructions}
            effort={ws.tasks[index].expected_effort_minutes}
            value={responses[ws.tasks[index].task_id] ?? ""}
            saveState={saveState}
            onChange={(text) => onType(ws.tasks[index].task_id, text)}
            onRetry={() => flush()}
          />
        )}

        {!reviewing && (
          <div className="flex items-center justify-between gap-3">
            <Button variant="outline" disabled={index === 0} onClick={() => go(index - 1)}>
              <ArrowLeft className="size-4" aria-hidden />
              Previous
            </Button>
            {index < total - 1 ? (
              <Button onClick={() => go(index + 1)}>
                Continue
                <ArrowRight className="size-4" aria-hidden />
              </Button>
            ) : (
              <Button onClick={() => go("review")}>
                Review
                <ArrowRight className="size-4" aria-hidden />
              </Button>
            )}
          </div>
        )}
      </div>
    </CandidateShell>
  );
}

function SaveStatus({ state }: { state: SaveState }) {
  if (state === "saving") {
    return (
      <span className="text-muted-foreground inline-flex items-center gap-1 text-xs">
        <Loader2 className="size-3.5 animate-spin" aria-hidden />
        Saving…
      </span>
    );
  }
  if (state === "unsaved") {
    return <span className="text-muted-foreground text-xs">Unsaved changes…</span>;
  }
  return (
    <span className="text-muted-foreground inline-flex items-center gap-1 text-xs">
      <Check className="text-success size-3.5" aria-hidden />
      Saved
    </span>
  );
}

function TaskScreen({
  prompt,
  instructions,
  effort,
  value,
  saveState,
  onChange,
  onRetry,
}: {
  prompt: string;
  instructions: string | null;
  effort: number | null;
  value: string;
  saveState: SaveState;
  onChange: (text: string) => void;
  onRetry: () => void;
}) {
  return (
    <FadeIn>
      <Card>
        <CardContent className="space-y-5 pt-6">
          <div className="space-y-2">
            <p className="text-[15px] leading-relaxed whitespace-pre-wrap">{prompt}</p>
            {instructions && (
              <p className="text-muted-foreground text-sm whitespace-pre-wrap">{instructions}</p>
            )}
            {effort != null && (
              <p className="text-muted-foreground text-xs">Estimated ~{effort} min</p>
            )}
          </div>
          <div className="space-y-1.5">
            <label htmlFor="response" className="text-sm font-medium">
              Your response
            </label>
            <Textarea
              id="response"
              value={value}
              onChange={(e) => onChange(e.target.value)}
              className="min-h-56"
              placeholder="Take your time — your work saves automatically."
            />
            <div className="flex items-center justify-between">
              {saveState === "error" ? (
                <button
                  type="button"
                  onClick={onRetry}
                  className="text-destructive text-xs font-medium hover:underline"
                >
                  Couldn’t save — your text is safe here. Retry
                </button>
              ) : (
                <SaveStatus state={saveState} />
              )}
              <span className="text-muted-foreground/70 text-xs tabular-nums">
                {value.trim().length} characters
              </span>
            </div>
          </div>
        </CardContent>
      </Card>
    </FadeIn>
  );
}

function ReviewScreen({
  ws,
  responses,
  submitting,
  onEdit,
  onSubmit,
}: {
  ws: CandidateWorkSample;
  responses: Record<string, string>;
  submitting: boolean;
  onEdit: (index: number) => void;
  onSubmit: () => void;
}) {
  const [confirm, setConfirm] = useState(false);
  const answeredCount = ws.tasks.filter((t) => answered(responses[t.task_id] ?? "")).length;
  const complete = answeredCount === ws.tasks.length;

  return (
    <FadeIn className="space-y-6">
      <Card>
        <CardContent className="space-y-4 pt-6">
          <div>
            <h2 className="text-lg font-semibold">Review your work</h2>
            <p className="text-muted-foreground text-sm">
              {answeredCount} of {ws.tasks.length} tasks complete
            </p>
          </div>
          <ul className="text-muted-foreground space-y-1 text-sm">
            <li>Make sure you’re happy with each response.</li>
            <li>After submission, you won’t be able to edit your work.</li>
            <li>Your responses are evaluated against the role-related criteria you reviewed.</li>
          </ul>
          <ul className="divide-y border-t">
            {ws.tasks.map((task, i) => {
              const done = answered(responses[task.task_id] ?? "");
              return (
                <li key={task.task_id} className="flex items-center justify-between gap-3 py-3">
                  <span className="flex items-center gap-2 text-sm">
                    {done ? (
                      <Check className="text-success size-4" aria-hidden />
                    ) : (
                      <CircleAlert className="text-warning size-4" aria-hidden />
                    )}
                    <span className="font-medium">Task {i + 1}</span>
                    <span className={done ? "text-muted-foreground" : "text-warning"}>
                      {done ? "Complete" : "Needs attention"}
                    </span>
                  </span>
                  <button
                    type="button"
                    onClick={() => onEdit(i)}
                    className="text-primary text-xs font-medium hover:underline"
                  >
                    {done ? "Review" : "Answer"}
                  </button>
                </li>
              );
            })}
          </ul>
        </CardContent>
      </Card>

      <div className="space-y-2">
        {!complete && (
          <p className="text-warning text-sm">Please answer every task before submitting.</p>
        )}
        <Button disabled={!complete} onClick={() => setConfirm(true)}>
          Submit work sample
        </Button>
        <p className="text-muted-foreground text-xs">
          Your work is saved. You can close this and return using your link.
        </p>
      </div>

      <Dialog open={confirm} onOpenChange={setConfirm}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Submit your work sample?</DialogTitle>
            <DialogDescription>
              After submission, your responses can no longer be edited.
            </DialogDescription>
          </DialogHeader>
          <div className="flex justify-end gap-2">
            <Button variant="ghost" onClick={() => setConfirm(false)} disabled={submitting}>
              Cancel
            </Button>
            <Button onClick={onSubmit} loading={submitting}>
              Submit work sample
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </FadeIn>
  );
}

function CompletionScreen({ completion }: { completion: Completion }) {
  return (
    <FadeIn>
      <Card>
        <CardContent className="flex flex-col items-center gap-5 px-6 py-12 text-center">
          <span className="bg-success/10 text-success flex size-14 items-center justify-center rounded-2xl">
            <CircleCheck className="size-7" aria-hidden />
          </span>
          <div className="space-y-1">
            <h1 className="text-2xl font-semibold tracking-tight">Work sample submitted</h1>
            <p className="text-muted-foreground">
              Thank you — your responses have been securely submitted.
            </p>
          </div>
          <p className="text-muted-foreground text-sm">
            {completion.organization_name} · {completion.role_title} · submitted{" "}
            {new Date(completion.submitted_at).toLocaleDateString()}
          </p>

          <div className="bg-secondary/50 w-full space-y-2 rounded-xl p-4 text-left text-sm">
            <p className="font-medium">What happens next</p>
            <ol className="text-muted-foreground list-decimal space-y-1 pl-5">
              <li>Your work is evaluated against the role-related criteria.</li>
              <li>AI may assist with analysis, but it doesn’t make the hiring decision.</li>
              <li>A person remains responsible for the hiring decision.</li>
            </ol>
          </div>
          <p className="text-muted-foreground text-xs">You can close this window.</p>
        </CardContent>
      </Card>
    </FadeIn>
  );
}

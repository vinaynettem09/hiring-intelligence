"use client";

import { ArrowRight, ShieldCheck } from "lucide-react";
import { useParams, useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import { toast } from "sonner";

import { CandidateProblem, problemForCode } from "@/components/candidate/candidate-problem";
import { CandidateShell } from "@/components/layout/candidate-shell";
import { FadeIn } from "@/components/motion/motion";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { ApiError } from "@/lib/api-client";
import { ConsentService } from "@/services/consent-service";
import type { ConsentState } from "@/types/consent";

type State =
  | { kind: "loading" }
  | { kind: "loaded"; data: ConsentState }
  | { kind: "problem"; code: string | null };

export default function ConsentPage() {
  const { token } = useParams<{ token: string }>();
  const router = useRouter();
  const [state, setState] = useState<State>({ kind: "loading" });
  const [checked, setChecked] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const load = useCallback(() => {
    setState({ kind: "loading" });
    ConsentService.getState(token)
      .then((res) => setState({ kind: "loaded", data: res.data }))
      .catch((e: unknown) =>
        setState({ kind: "problem", code: e instanceof ApiError ? e.body.code : null }),
      );
  }, [token]);

  useEffect(() => {
    load();
  }, [load]);

  async function onContinue() {
    setSubmitting(true);
    try {
      await ConsentService.grant(token); // idempotent; backend is the source of truth
      router.push(`/invite/${token}/work-sample`);
    } catch (e: unknown) {
      setSubmitting(false);
      if (e instanceof ApiError && e.body.code?.startsWith("INVITATION_")) {
        setState({ kind: "problem", code: e.body.code });
        return;
      }
      toast.error("Something went wrong. Please try again.");
    }
  }

  return (
    <CandidateShell>
      {state.kind === "loading" && (
        <div className="space-y-4">
          <Skeleton className="h-7 w-2/3" />
          <Skeleton className="h-64 w-full rounded-xl" />
        </div>
      )}

      {state.kind === "problem" && (
        <CandidateProblem
          {...problemForCode(state.code)}
          action={
            state.code === null ? (
              <Button variant="outline" onClick={load}>
                Try again
              </Button>
            ) : undefined
          }
        />
      )}

      {state.kind === "loaded" && (
        <FadeIn className="space-y-6">
          <div className="space-y-1">
            <p className="text-muted-foreground text-sm">
              {state.data.organization_name} · {state.data.role_title}
            </p>
            <h1 className="text-2xl font-semibold tracking-tight">Before you continue</h1>
            <p className="text-muted-foreground">
              Here’s exactly how your work sample will be used. Please review, then give your
              consent to continue.
            </p>
          </div>

          <Card>
            <CardContent className="divide-y pt-2">
              {state.data.disclosure.sections.map((section) => (
                <div key={section.key} className="py-3">
                  <p className="text-sm font-medium">{section.title}</p>
                  <p className="text-muted-foreground mt-0.5 text-sm">{section.body}</p>
                </div>
              ))}
            </CardContent>
          </Card>

          {state.data.consented ? (
            <div className="flex flex-col gap-3">
              <p className="text-muted-foreground flex items-center gap-2 text-sm">
                <ShieldCheck className="text-success size-4" aria-hidden />
                You’ve already consented to this.
              </p>
              <Button className="w-fit" onClick={onContinue} loading={submitting}>
                Continue to work sample
                <ArrowRight className="size-4" aria-hidden />
              </Button>
            </div>
          ) : (
            <div className="space-y-4">
              <label
                htmlFor="consent"
                className="hover:bg-muted/40 flex cursor-pointer items-start gap-3 rounded-lg border p-4"
              >
                <input
                  id="consent"
                  type="checkbox"
                  checked={checked}
                  onChange={(e) => setChecked(e.target.checked)}
                  className="accent-primary mt-0.5 size-4"
                />
                <span className="text-sm">
                  I understand and consent to the use of my work-sample submission as described
                  above.
                </span>
              </label>
              <Button disabled={!checked} loading={submitting} onClick={onContinue}>
                Continue to work sample
                <ArrowRight className="size-4" aria-hidden />
              </Button>
            </div>
          )}

          <p className="text-muted-foreground/70 text-xs">
            Consent version {state.data.disclosure.version}
          </p>
        </FadeIn>
      )}
    </CandidateShell>
  );
}

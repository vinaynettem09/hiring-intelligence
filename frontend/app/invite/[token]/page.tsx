"use client";

import { ArrowRight, ClipboardCheck, FileText, ShieldCheck, type LucideIcon } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useCallback, useEffect, useState } from "react";

import { CandidateProblem, problemForCode } from "@/components/candidate/candidate-problem";
import { CandidateShell } from "@/components/layout/candidate-shell";
import { FadeIn } from "@/components/motion/motion";
import { Button, buttonVariants } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { ApiError } from "@/lib/api-client";
import { cn } from "@/lib/utils";
import { InvitationService } from "@/services/invitation-service";
import type { CandidateInvitationView } from "@/types/invitation";

type State =
  | { kind: "loading" }
  | { kind: "valid"; view: CandidateInvitationView }
  | { kind: "problem"; code: string | null };

export default function InvitePage() {
  const { token } = useParams<{ token: string }>();
  const [state, setState] = useState<State>({ kind: "loading" });

  const load = useCallback(() => {
    setState({ kind: "loading" });
    InvitationService.resolve(token)
      .then((res) => setState({ kind: "valid", view: res.data }))
      .catch((e: unknown) =>
        setState({ kind: "problem", code: e instanceof ApiError ? e.body.code : null }),
      );
  }, [token]);

  useEffect(() => {
    load();
  }, [load]);

  return (
    <CandidateShell>
      {state.kind === "loading" && (
        <div className="space-y-4">
          <Skeleton className="h-7 w-2/3" />
          <Skeleton className="h-40 w-full rounded-xl" />
          <Skeleton className="h-11 w-40 rounded-lg" />
        </div>
      )}

      {state.kind === "valid" && <ValidInvitation token={token} view={state.view} />}

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
    </CandidateShell>
  );
}

function ValidInvitation({ token, view }: { token: string; view: CandidateInvitationView }) {
  const expires = new Date(view.expires_at).toLocaleDateString();
  const firstName = view.candidate_name.split(" ")[0] || "there";

  return (
    <FadeIn className="space-y-6">
      <div className="space-y-2">
        <p className="text-muted-foreground text-sm">Hi {firstName},</p>
        <h1 className="text-2xl font-semibold tracking-tight text-balance">
          {view.organization_name} invited you to a work sample
        </h1>
        <p className="text-muted-foreground">
          for the <span className="text-foreground font-medium">{view.role_title}</span> role — a
          chance to show your skills through real work, not just a résumé.
        </p>
      </div>

      <Card>
        <CardContent className="space-y-4 pt-6">
          <Step
            icon={ClipboardCheck}
            title="Review & consent"
            body="First, you’ll review a few details and give your consent. Takes a minute."
          />
          <Step
            icon={FileText}
            title="Complete a short work sample"
            body="A focused, text-based exercise you can do at your own pace."
          />
          <Step
            icon={ShieldCheck}
            title="A person makes the decision"
            body="Your work is reviewed by the hiring team. AI may assist, but a human decides."
          />
        </CardContent>
      </Card>

      <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
        <Link href={`/invite/${token}/consent`} className={cn(buttonVariants({ size: "lg" }))}>
          Review &amp; continue
          <ArrowRight className="size-4" aria-hidden />
        </Link>
        <p className="text-muted-foreground text-xs">This link is personal to you · expires {expires}</p>
      </div>
    </FadeIn>
  );
}

function Step({ icon: Icon, title, body }: { icon: LucideIcon; title: string; body: string }) {
  return (
    <div className="flex gap-3">
      <span className="bg-secondary text-primary flex size-9 shrink-0 items-center justify-center rounded-lg">
        <Icon className="size-4" aria-hidden />
      </span>
      <div className="space-y-0.5">
        <p className="text-sm font-medium">{title}</p>
        <p className="text-muted-foreground text-sm">{body}</p>
      </div>
    </div>
  );
}


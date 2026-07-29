"use client";

import {
  ArrowRight,
  FileText,
  Gavel,
  ListChecks,
  Sparkles,
  type LucideIcon,
} from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";

import { FadeIn } from "@/components/motion/motion";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { HealthService } from "@/services/health-service";
import type { HealthResponse } from "@/types/health";

// The four real steps of the product — the thesis, stated plainly. No fabricated logos,
// stats, or claims we haven't validated.
const STEPS: Array<{ icon: LucideIcon; title: string; body: string }> = [
  { icon: ListChecks, title: "Define what matters", body: "The role's competencies and the bar to clear." },
  { icon: FileText, title: "Collect work evidence", body: "Candidates complete a structured work sample." },
  { icon: Sparkles, title: "Evidence-cited AI", body: "An assessment tied to what they actually did." },
  { icon: Gavel, title: "You decide", body: "The recommendation is advisory. A human decides." },
];

export default function Home() {
  const [health, setHealth] = useState<HealthResponse | null>(null);

  useEffect(() => {
    HealthService.get()
      .then((res) => setHealth(res.data))
      .catch(() => setHealth(null)); // health line is optional on the landing
  }, []);

  return (
    <main className="bg-spotlight flex min-h-screen flex-col items-center justify-center gap-10 px-4 py-16 text-center">
      <FadeIn className="flex flex-col items-center gap-6">
        <span className="bg-card/60 flex items-center gap-1.5 rounded-full border px-3 py-1 text-xs font-medium backdrop-blur">
          <Sparkles className="text-primary size-3.5" aria-hidden />
          Evidence-based hiring
        </span>
        <h1 className="max-w-2xl text-4xl font-semibold tracking-tight text-balance sm:text-5xl">
          Hire on evidence of how people work — not résumé keywords.
        </h1>
        <p className="text-muted-foreground max-w-xl text-lg text-balance">
          Candidates complete a real work sample. The AI proposes an assessment cited to their
          actual work. Your team makes the decision.
        </p>
        <div className="flex flex-wrap items-center justify-center gap-3">
          <Link href="/signup" className={cn(buttonVariants({ size: "lg" }))}>
            Get started
            <ArrowRight className="size-4" aria-hidden />
          </Link>
          <Link href="/login" className={cn(buttonVariants({ variant: "outline", size: "lg" }))}>
            Log in
          </Link>
        </div>
      </FadeIn>

      <FadeIn delay={0.1} className="grid w-full max-w-3xl grid-cols-2 gap-3 lg:grid-cols-4">
        {STEPS.map((step, i) => (
          <div key={step.title} className="bg-card/50 rounded-xl border p-4 text-left backdrop-blur">
            <div className="text-muted-foreground mb-2 flex items-center gap-2 text-xs font-medium">
              <span className="bg-secondary text-primary flex size-6 items-center justify-center rounded-md">
                <step.icon className="size-3.5" aria-hidden />
              </span>
              Step {i + 1}
            </div>
            <p className="text-sm font-medium">{step.title}</p>
            <p className="text-muted-foreground mt-0.5 text-xs leading-relaxed">{step.body}</p>
          </div>
        ))}
      </FadeIn>

      {health && (
        <p className="text-muted-foreground/70 text-xs">
          Backend {health.status} · v{health.version}
        </p>
      )}
    </main>
  );
}

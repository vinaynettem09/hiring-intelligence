"use client";

import { Check, Loader2, Sparkles } from "lucide-react";
import { useEffect, useState } from "react";

import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

// A designed processing state — not a bare spinner. It reveals the phases of a real
// evaluation as restrained, staged messaging. It does NOT display a fake backend
// percentage; the steps advance on a gentle timer and hold on the final phase until the
// real result arrives (then the parent swaps this out).
const STEPS = [
  "Reading work-sample evidence",
  "Comparing evidence with role criteria",
  "Building grounded assessment",
];

export function EvaluationGeneratingState() {
  const [active, setActive] = useState(0);

  useEffect(() => {
    if (active >= STEPS.length - 1) return;
    const timer = setTimeout(() => setActive((i) => Math.min(i + 1, STEPS.length - 1)), 1800);
    return () => clearTimeout(timer);
  }, [active]);

  return (
    <Card className="p-8">
      <div className="text-primary mb-6 flex items-center gap-2 text-sm font-medium">
        <Sparkles className="size-4" aria-hidden />
        Reviewing submitted evidence&hellip;
      </div>
      <ul className="space-y-4" aria-live="polite">
        {STEPS.map((step, i) => {
          const done = i < active;
          const current = i === active;
          return (
            <li
              key={step}
              className={cn(
                "flex items-center gap-3 text-sm transition-colors",
                current ? "text-foreground" : done ? "text-muted-foreground" : "text-muted-foreground/40",
              )}
            >
              <span className="flex size-5 items-center justify-center">
                {done ? (
                  <Check className="text-success size-4" aria-hidden />
                ) : current ? (
                  <Loader2 className="text-primary size-4 animate-spin motion-reduce:animate-none" aria-hidden />
                ) : (
                  <span className="bg-muted-foreground/30 size-1.5 rounded-full" aria-hidden />
                )}
              </span>
              {step}
              {current && <span className="sr-only">in progress</span>}
            </li>
          );
        })}
      </ul>
      <p className="text-muted-foreground mt-6 text-xs">
        This usually takes a few moments. The evaluation is generated from the candidate&rsquo;s
        submitted evidence only.
      </p>
    </Card>
  );
}

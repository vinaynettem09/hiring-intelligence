import { Sparkles } from "lucide-react";
import type { ReactNode } from "react";

// The candidate's frame — deliberately distinct from the recruiter AppShell: no
// navigation, no account, just a calm, centered, trustworthy surface. Mobile-first.
export function CandidateShell({ children }: { children: ReactNode }) {
  return (
    <div className="bg-spotlight flex min-h-screen flex-col">
      <header className="flex items-center justify-center py-6">
        <span className="text-muted-foreground flex items-center gap-2 text-sm font-medium">
          <span className="bg-primary text-primary-foreground flex size-6 items-center justify-center rounded-md">
            <Sparkles className="size-3.5" aria-hidden />
          </span>
          Hiring Intelligence
        </span>
      </header>
      <main className="mx-auto flex w-full max-w-xl flex-1 flex-col justify-center px-4 pb-16">
        {children}
      </main>
    </div>
  );
}

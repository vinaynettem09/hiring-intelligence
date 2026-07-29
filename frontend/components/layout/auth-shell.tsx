import { Sparkles } from "lucide-react";
import Link from "next/link";
import type { ReactNode } from "react";

// Centered, calm frame for auth screens — brand mark over a single card, on a
// faint spotlight wash.
export function AuthShell({ children }: { children: ReactNode }) {
  return (
    <div className="bg-spotlight flex min-h-screen flex-col items-center justify-center gap-8 px-4 py-12">
      <Link href="/" className="flex items-center gap-2 text-sm font-semibold">
        <span className="bg-primary text-primary-foreground flex size-8 items-center justify-center rounded-lg">
          <Sparkles className="size-4" aria-hidden />
        </span>
        Hiring Intelligence
      </Link>
      <div className="w-full max-w-sm">{children}</div>
    </div>
  );
}

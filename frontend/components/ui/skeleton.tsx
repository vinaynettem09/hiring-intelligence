import { cn } from "@/lib/utils";

/** A calm loading placeholder — pulses subtly, never a jarring spinner-on-blank. */
export function Skeleton({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("bg-muted animate-pulse rounded-md", className)} {...props} />;
}

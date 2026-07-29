import { AlertTriangle } from "lucide-react";
import type { ReactNode } from "react";

// Errors are never a JSON dump: a clear title, a human explanation, a way to
// recover, and a small correlation id for support.
export function ErrorState({
  title = "Something went wrong",
  message,
  correlationId,
  action,
}: {
  title?: string;
  message: string;
  correlationId?: string | null;
  action?: ReactNode;
}) {
  return (
    <div className="border-destructive/30 bg-destructive/5 flex flex-col items-center justify-center gap-3 rounded-xl border px-6 py-10 text-center">
      <AlertTriangle className="text-destructive size-6" aria-hidden />
      <div className="space-y-1">
        <p className="font-medium">{title}</p>
        <p className="text-muted-foreground mx-auto max-w-sm text-sm">{message}</p>
      </div>
      {action}
      {correlationId && (
        <p className="text-muted-foreground/70 font-mono text-[11px]">ref: {correlationId}</p>
      )}
    </div>
  );
}

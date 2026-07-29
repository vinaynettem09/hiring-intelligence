import { FlaskConical } from "lucide-react";

// Mock intelligence must never masquerade as real. When the run came from the deterministic
// mock provider, say so unmistakably. Real providers (Gemini/Anthropic/...) are NOT marketed
// in the primary UX — the provider belongs in Evaluation details.
export function MockEvaluationNotice({ provider }: { provider: string }) {
  if (provider !== "mock") return null;
  return (
    <div className="border-warning/40 bg-warning/10 text-warning flex items-start gap-2 rounded-lg border px-4 py-3 text-sm">
      <FlaskConical className="mt-0.5 size-4 shrink-0" aria-hidden />
      <p>
        <span className="font-semibold">Mock evaluation &mdash; development only.</span> This is
        deterministic placeholder output, not a real model assessment. Do not use it to make
        decisions.
      </p>
    </div>
  );
}

import { cn } from "@/lib/utils";

// A single headline metric — the "what's here / needs attention" building block.
export function Stat({
  label,
  value,
  tone = "default",
}: {
  label: string;
  value: string | number;
  tone?: "default" | "attention";
}) {
  const highlight = tone === "attention" && Number(value) > 0;
  return (
    <div className="bg-card rounded-xl border p-4 shadow-subtle">
      <p className={cn("text-2xl font-semibold tabular-nums", highlight && "text-warning")}>{value}</p>
      <p className="text-muted-foreground text-sm">{label}</p>
    </div>
  );
}

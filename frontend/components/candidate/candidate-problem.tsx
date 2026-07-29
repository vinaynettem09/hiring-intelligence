import { AlertTriangle, CalendarClock, CircleSlash, type LucideIcon } from "lucide-react";
import type { ReactNode } from "react";

import { FadeIn } from "@/components/motion/motion";
import { Card, CardContent } from "@/components/ui/card";

// A single, humane problem card for candidate pages — never leaks security detail.
export function CandidateProblem({
  icon: Icon,
  title,
  body,
  action,
}: {
  icon: LucideIcon;
  title: string;
  body: string;
  action?: ReactNode;
}) {
  return (
    <FadeIn>
      <Card>
        <CardContent className="flex flex-col items-center gap-4 px-6 py-12 text-center">
          <span className="bg-secondary text-muted-foreground flex size-12 items-center justify-center rounded-full">
            <Icon className="size-6" aria-hidden />
          </span>
          <div className="space-y-1">
            <h1 className="text-lg font-semibold">{title}</h1>
            <p className="text-muted-foreground mx-auto max-w-sm text-sm">{body}</p>
          </div>
          {action}
        </CardContent>
      </Card>
    </FadeIn>
  );
}

/** Maps a backend invitation error code (or null = network) to humane, non-leaky copy. */
export function problemForCode(code: string | null): {
  icon: LucideIcon;
  title: string;
  body: string;
} {
  switch (code) {
    case "INVITATION_EXPIRED":
      return {
        icon: CalendarClock,
        title: "This invitation has expired",
        body: "Invitation links are time-limited. Ask the company to send you a fresh link to continue.",
      };
    case "INVITATION_REVOKED":
      return {
        icon: CircleSlash,
        title: "This invitation is no longer active",
        body: "A newer invitation may have been sent to your email. Please use the most recent link.",
      };
    case "INVITATION_INVALID":
      return {
        icon: CircleSlash,
        title: "This invitation link isn’t valid",
        body: "Please double-check the link from your email, or ask the company to resend it.",
      };
    default:
      return {
        icon: AlertTriangle,
        title: "Something went wrong",
        body: "We couldn’t load this just now. Please try again in a moment.",
      };
  }
}

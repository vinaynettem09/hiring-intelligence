"use client";

import { LayoutGrid, Plus } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";

import { EmptyState } from "@/components/feedback/empty-state";
import { ErrorState } from "@/components/feedback/error-state";
import { PageHeader } from "@/components/layout/page-header";
import { StaggerItem, StaggerList } from "@/components/motion/motion";
import { StatusBadge } from "@/components/status-badge";
import { Button, buttonVariants } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { ApiError } from "@/lib/api-client";
import { authStore } from "@/lib/auth-store";
import { cn } from "@/lib/utils";
import { CampaignService } from "@/services/campaign-service";
import type { CampaignListResponse } from "@/types/campaign";

export default function CampaignsPage() {
  const router = useRouter();
  const [data, setData] = useState<CampaignListResponse | null>(null);
  const [error, setError] = useState<{ message: string; correlationId: string | null } | null>(null);
  const [loading, setLoading] = useState(true);

  const load = useCallback(() => {
    setLoading(true);
    setError(null);
    CampaignService.list({ limit: 20 })
      .then((res) => setData(res.data))
      .catch((e: unknown) => {
        if (e instanceof ApiError && e.status === 401) {
          router.replace("/login");
          return;
        }
        setError({
          message: e instanceof Error ? e.message : "Failed to load campaigns",
          correlationId: e instanceof ApiError ? e.body.correlation_id : null,
        });
      })
      .finally(() => setLoading(false));
  }, [router]);

  useEffect(() => {
    if (!authStore.getAccess()) {
      router.replace("/login");
      return;
    }
    load();
  }, [load, router]);

  const newCampaign = (
    <Link href="/campaigns/new" className={cn(buttonVariants())}>
      <Plus className="size-4" aria-hidden />
      New campaign
    </Link>
  );

  return (
    <div className="space-y-8">
      <PageHeader
        title="Campaigns"
        description="Your organization’s evaluation campaigns."
        actions={data && data.items.length > 0 ? newCampaign : undefined}
      />

      {loading && (
        <div className="space-y-3">
          {[0, 1, 2].map((i) => (
            <Skeleton key={i} className="h-[68px] w-full rounded-xl" />
          ))}
        </div>
      )}

      {!loading && error && (
        <ErrorState
          message={error.message}
          correlationId={error.correlationId}
          action={
            <Button variant="outline" size="sm" onClick={load}>
              Try again
            </Button>
          }
        />
      )}

      {!loading && !error && data && data.items.length === 0 && (
        <EmptyState
          icon={LayoutGrid}
          title="No campaigns yet"
          description="Create your first evaluation campaign to start assessing candidates on real work."
          action={newCampaign}
        />
      )}

      {!loading && !error && data && data.items.length > 0 && (
        <div className="space-y-4">
          <StaggerList className="space-y-3">
            {data.items.map((c) => (
              <StaggerItem key={c.id}>
                <Link href={`/campaigns/${c.id}`} className="block">
                  <Card className="hover:shadow-elevated flex items-center justify-between gap-4 p-4 transition-shadow">
                    <div className="min-w-0">
                      <p className="truncate font-medium">{c.role_title}</p>
                      <p className="text-muted-foreground text-xs">
                        Created {new Date(c.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    <StatusBadge status={c.status} />
                  </Card>
                </Link>
              </StaggerItem>
            ))}
          </StaggerList>
          <p className="text-muted-foreground text-xs">
            Showing {data.items.length} of {data.total}.
          </p>
        </div>
      )}
    </div>
  );
}

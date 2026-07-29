"use client";

import { usePathname, useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";

import { authStore } from "@/lib/auth-store";
import { IdentityService } from "@/services/identity-service";
import type { MeResponse } from "@/types/identity";

import { BreadcrumbProvider, Breadcrumbs } from "./breadcrumbs";
import { MobileNav } from "./mobile-nav";
import { Sidebar } from "./sidebar";

const COLLAPSE_KEY = "hi.sidebar.collapsed";

// The authenticated application shell: a premium responsive frame around every recruiter
// destination. Desktop = collapsible sidebar + a breadcrumb context bar on deep pages;
// mobile = top bar + slide-in drawer. Only real destinations; the design system does the
// rest. This is the single shell — pages render their own content unchanged.
export function AppShell({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const [identity, setIdentity] = useState<MeResponse | null>(null);
  const [collapsed, setCollapsed] = useState(false);

  useEffect(() => {
    setCollapsed(localStorage.getItem(COLLAPSE_KEY) === "1");
    // Best-effort: powers the account block. Failure never blocks the shell (pages own auth).
    IdentityService.getMe()
      .then((r) => setIdentity(r.data))
      .catch(() => undefined);
  }, []);

  const toggleCollapse = useCallback(() => {
    setCollapsed((c) => {
      const next = !c;
      localStorage.setItem(COLLAPSE_KEY, next ? "1" : "0");
      return next;
    });
  }, []);

  const onLogout = useCallback(async () => {
    const refresh = authStore.getRefresh();
    try {
      if (refresh) await IdentityService.logout({ refresh_token: refresh });
    } catch {
      /* best-effort revoke — clear locally regardless */
    }
    authStore.clear();
    router.replace("/login");
  }, [router]);

  const deep = pathname.split("/").filter(Boolean).length > 1;

  return (
    <BreadcrumbProvider>
      <div className="flex min-h-screen">
        <Sidebar
          identity={identity}
          onLogout={onLogout}
          collapsed={collapsed}
          onToggleCollapse={toggleCollapse}
        />
        <div className="flex min-w-0 flex-1 flex-col">
          <MobileNav identity={identity} onLogout={onLogout} />
          {deep && (
            <div className="bg-background/70 sticky top-0 z-20 hidden h-12 items-center border-b px-6 backdrop-blur-md lg:flex">
              <Breadcrumbs />
            </div>
          )}
          <main className="mx-auto w-full max-w-5xl flex-1 px-4 py-8 sm:px-6 sm:py-10">
            {children}
          </main>
        </div>
      </div>
    </BreadcrumbProvider>
  );
}

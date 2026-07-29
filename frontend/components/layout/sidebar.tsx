"use client";

import { ChevronsLeft, ChevronsRight, LogOut, Sparkles } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

import { ThemeToggle } from "@/components/theme/theme-toggle";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import type { MeResponse } from "@/types/identity";

import { NAV_ITEMS, isActive } from "./nav-items";

// The desktop application shell rail. Collapsible to icons-only; only real destinations;
// account + theme + logout anchored at the foot. Screen readers always get the full label
// (kept as sr-only when collapsed).
export function Sidebar({
  identity,
  onLogout,
  collapsed,
  onToggleCollapse,
}: {
  identity: MeResponse | null;
  onLogout: () => void;
  collapsed: boolean;
  onToggleCollapse: () => void;
}) {
  const pathname = usePathname();

  return (
    <aside
      className={cn(
        "bg-card sticky top-0 hidden h-screen shrink-0 flex-col border-r lg:flex",
        collapsed ? "w-16" : "w-60",
      )}
    >
      <Link
        href="/dashboard"
        className={cn(
          "flex h-14 items-center gap-2 border-b px-4 text-sm font-semibold",
          collapsed && "justify-center px-0",
        )}
      >
        <span className="bg-primary text-primary-foreground flex size-7 shrink-0 items-center justify-center rounded-lg">
          <Sparkles className="size-4" aria-hidden />
        </span>
        <span className={cn(collapsed && "sr-only")}>Hiring Intelligence</span>
      </Link>

      <nav className="flex-1 space-y-1 p-3" aria-label="Primary">
        {NAV_ITEMS.map((item) => {
          const active = isActive(pathname, item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              aria-current={active ? "page" : undefined}
              title={collapsed ? item.label : undefined}
              className={cn(
                "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                collapsed && "justify-center px-0",
                active
                  ? "bg-secondary text-foreground"
                  : "text-muted-foreground hover:text-foreground hover:bg-muted",
              )}
            >
              <item.icon className="size-4 shrink-0" aria-hidden />
              <span className={cn(collapsed && "sr-only")}>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className="space-y-2 border-t p-3">
        {identity && !collapsed && (
          <div className="px-1">
            <p className="truncate text-sm font-medium">{identity.organization.name}</p>
            <p className="text-muted-foreground truncate text-xs">{identity.email}</p>
          </div>
        )}
        <div className={cn("flex items-center gap-1", collapsed ? "flex-col" : "justify-between")}>
          <ThemeToggle />
          <Button
            variant="ghost"
            size={collapsed ? "icon" : "sm"}
            onClick={onLogout}
            title="Log out"
          >
            <LogOut className="size-4" aria-hidden />
            <span className={cn(collapsed && "sr-only")}>Log out</span>
          </Button>
        </div>
        <Button
          variant="ghost"
          size={collapsed ? "icon" : "sm"}
          onClick={onToggleCollapse}
          aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
          className={cn(!collapsed && "w-full justify-start")}
        >
          {collapsed ? (
            <ChevronsRight className="size-4" aria-hidden />
          ) : (
            <ChevronsLeft className="size-4" aria-hidden />
          )}
          <span className={cn(collapsed && "sr-only")}>Collapse</span>
        </Button>
      </div>
    </aside>
  );
}

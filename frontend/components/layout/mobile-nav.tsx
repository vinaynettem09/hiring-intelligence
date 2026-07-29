"use client";

import * as DialogPrimitive from "@radix-ui/react-dialog";
import { LogOut, Menu, Sparkles, X } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

import { ThemeToggle } from "@/components/theme/theme-toggle";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import type { MeResponse } from "@/types/identity";

import { NAV_ITEMS, isActive } from "./nav-items";

// Mobile: a slim top bar with a hamburger that opens a left slide-in drawer holding the
// same real destinations + account/theme/logout. Closes on navigation. Reduced-motion safe.
export function MobileNav({
  identity,
  onLogout,
}: {
  identity: MeResponse | null;
  onLogout: () => void;
}) {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  // Close the drawer whenever the route changes.
  useEffect(() => {
    setOpen(false);
  }, [pathname]);

  return (
    <div className="flex h-14 items-center justify-between gap-2 border-b px-4 lg:hidden">
      <DialogPrimitive.Root open={open} onOpenChange={setOpen}>
        <DialogPrimitive.Trigger asChild>
          <Button variant="ghost" size="icon" aria-label="Open navigation">
            <Menu className="size-5" aria-hidden />
          </Button>
        </DialogPrimitive.Trigger>
        <DialogPrimitive.Portal>
          <DialogPrimitive.Overlay className="data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 motion-reduce:animate-none fixed inset-0 z-50 bg-black/40 backdrop-blur-sm" />
          <DialogPrimitive.Content className="bg-card data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:slide-out-to-left data-[state=open]:slide-in-from-left motion-reduce:animate-none fixed inset-y-0 left-0 z-50 flex w-72 max-w-[85vw] flex-col border-r">
            <DialogPrimitive.Title className="sr-only">Navigation</DialogPrimitive.Title>
            <div className="flex h-14 items-center justify-between border-b px-4">
              <span className="flex items-center gap-2 text-sm font-semibold">
                <span className="bg-primary text-primary-foreground flex size-7 items-center justify-center rounded-lg">
                  <Sparkles className="size-4" aria-hidden />
                </span>
                Hiring Intelligence
              </span>
              <DialogPrimitive.Close asChild>
                <Button variant="ghost" size="icon" aria-label="Close navigation">
                  <X className="size-5" aria-hidden />
                </Button>
              </DialogPrimitive.Close>
            </div>

            <nav className="flex-1 space-y-1 p-3" aria-label="Primary">
              {NAV_ITEMS.map((item) => {
                const active = isActive(pathname, item.href);
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    aria-current={active ? "page" : undefined}
                    className={cn(
                      "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                      active
                        ? "bg-secondary text-foreground"
                        : "text-muted-foreground hover:text-foreground hover:bg-muted",
                    )}
                  >
                    <item.icon className="size-4 shrink-0" aria-hidden />
                    {item.label}
                  </Link>
                );
              })}
            </nav>

            <div className="space-y-2 border-t p-3">
              {identity && (
                <div className="px-1">
                  <p className="truncate text-sm font-medium">{identity.organization.name}</p>
                  <p className="text-muted-foreground truncate text-xs">{identity.email}</p>
                </div>
              )}
              <div className="flex items-center justify-between">
                <ThemeToggle />
                <Button variant="ghost" size="sm" onClick={onLogout}>
                  <LogOut className="size-4" aria-hidden />
                  Log out
                </Button>
              </div>
            </div>
          </DialogPrimitive.Content>
        </DialogPrimitive.Portal>
      </DialogPrimitive.Root>

      <Link href="/dashboard" className="flex items-center gap-2 text-sm font-semibold">
        <span className="bg-primary text-primary-foreground flex size-7 items-center justify-center rounded-lg">
          <Sparkles className="size-4" aria-hidden />
        </span>
        <span className="hidden sm:inline">Hiring Intelligence</span>
      </Link>

      <ThemeToggle />
    </div>
  );
}

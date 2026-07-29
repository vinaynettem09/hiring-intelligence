import { Inbox, LayoutDashboard, LayoutGrid, type LucideIcon } from "lucide-react";

// The authenticated product's navigation — the SINGLE source of truth, shared by the
// desktop sidebar and the mobile drawer. Only REAL destinations live here; we do not
// invent Settings / Analytics / Reports to fill space. Dashboard = overview, Review =
// daily operational work, Campaigns = setup (with campaign/candidate/evaluation beneath).
export interface NavItem {
  href: string;
  label: string;
  icon: LucideIcon;
}

export const NAV_ITEMS: NavItem[] = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/review-queue", label: "Review", icon: Inbox },
  { href: "/campaigns", label: "Campaigns", icon: LayoutGrid },
];

/** Whether a nav item is active for the current path (its section, including deep pages). */
export function isActive(pathname: string, href: string): boolean {
  return pathname === href || pathname.startsWith(`${href}/`);
}

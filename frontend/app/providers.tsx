"use client";

import { ThemeProvider } from "next-themes";
import { Toaster } from "sonner";

// App-wide client providers: theme (light/dark, system-aware) + toasts.
export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
      {children}
      <Toaster position="top-right" richColors closeButton />
    </ThemeProvider>
  );
}

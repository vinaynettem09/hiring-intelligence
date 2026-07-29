import { fileURLToPath } from "node:url";

import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

// Component/unit test harness for the frontend. Protects behavioral contracts (presentation
// vocabulary, the AI/human-decision boundary, navigation, forms) — not snapshots or coverage %.
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { "@": fileURLToPath(new URL(".", import.meta.url)) },
  },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./vitest.setup.ts"],
    include: ["{app,components,lib}/**/*.test.{ts,tsx}"],
    exclude: ["node_modules", ".next"],
    css: false,
    clearMocks: true,
  },
});

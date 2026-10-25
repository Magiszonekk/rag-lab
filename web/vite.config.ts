import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// base "./": build działa z dowolnej ścieżki (Azure SWA albo serwer domowy), routing po hashu.
export default defineConfig({
  base: "./",
  plugins: [react()],
  server: { port: 5173, fs: { allow: [".."] } },
  build: { outDir: "dist", sourcemap: false },
});

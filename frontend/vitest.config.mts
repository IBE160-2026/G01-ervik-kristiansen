import { fileURLToPath } from 'node:url';

import { defineConfig } from 'vitest/config';

// Aliaset `@/*` fra tsconfig.json, så kode under `src/` som importerer med `@/` virker i testene.
export default defineConfig({
  resolve: {
    alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) },
  },
});

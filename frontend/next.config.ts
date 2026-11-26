import type { NextConfig } from 'next';

// Statisk eksport (AD-9): `npm run build` lager `out/`, som FastAPI eller Vercel serverer.
// `trailingSlash: true` gir `out/anlegg/index.html`, slik at detaljsiden `/anlegg/?nr=…` virker ved
// direkte lasting. `/anlegg?nr=…` uten skråstrek virker bare når verten omdirigerer `/anlegg` til `/anlegg/`.
const nextConfig: NextConfig = {
  output: 'export',
  trailingSlash: true,
};

export default nextConfig;

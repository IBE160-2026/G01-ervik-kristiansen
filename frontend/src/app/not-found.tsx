import Link from 'next/link';

import { tekster } from '@/tekster';

/**
 * 404-siden for stier som ikke finnes. `npm run build` lager `out/404.html` av den, og
 * FastAPI og Vercel viser den for ukjente sider. Den erstatter standardsiden til Next, som
 * er på engelsk og har mørk modus. Rotlayouten gir `lang="nb"` og grunnreglene.
 */
export default function IkkeFunnet() {
  return (
    <main className="mx-auto max-w-content-max-width px-page-x-mobile pt-page-top-mobile pb-page-bottom-mobile desktop:px-page-x desktop:pt-page-top desktop:pb-page-bottom">
      <h1 className="text-title-mobile desktop:text-title">{tekster.ikkeFunnet.overskrift}</h1>
      <p className="mt-heading-gap">
        {/* Trykkflaten er minst 44px høy på mobil og 24px på desktop (DESIGN.md). */}
        <Link href="/" className="inline-flex items-center min-h-target-min desktop:min-h-target-min-inline">
          {tekster.ikkeFunnet.tilForsiden}
        </Link>
      </p>
    </main>
  );
}

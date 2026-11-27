/**
 * Komponentene bruker bare tokennavn fra `@theme` (DESIGN.md). Sjekken leser alle kode-, CSS- og
 * SVG-filer under `src/`, også kommentarene, og feiler ved fargekoder, lengder i px, rem og em,
 * fontnavn, breddeklasser med tall og klasser med egne verdier i hakeparentes. `app/globals.css`,
 * der tokenene står, og den genererte `api/schema.ts` er unntatt. Den sjekker også at bare
 * filene under `api/` kaller `fetch` (AD-3).
 */
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

import { describe, expect, it } from 'vitest';

const SRC = fileURLToPath(new URL('../src/', import.meta.url));
const UNNTATT = ['app/globals.css', 'api/schema.ts'];
const ENDELSER = ['.ts', '.tsx', '.js', '.jsx', '.mjs', '.css', '.svg'];

/**
 * Treff som er lov likevel, skrevet slik de står i fila. Lista er tom. Velger Story 2.4
 * `font-[600]` framfor egne vekttokens, legges klassen inn her.
 */
const TILLATT: readonly string[] = [];

/** Fontnavnene i `--font-sans`, uten anførselstegn, for eksempel `Segoe UI` og `Arial`. */
function fontnavn(): string[] {
  const css = readFileSync(join(SRC, 'app', 'globals.css'), 'utf8');
  const stabel = /--font-sans:([^;]+);/.exec(css)?.[1];
  if (stabel === undefined) {
    throw new Error('fant ikke --font-sans i globals.css');
  }
  return stabel
    .split(',')
    .map((navn) => navn.trim().replace(/^["']|["']$/g, ''))
    .filter((navn) => navn !== '');
}

function somRegex(tekst: string): string {
  return tekst.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/** Mønstrene for egne verdier. Fontnavnene står hele, så `font-sans` ikke gir treff. */
function monstre(fonter: readonly string[]): RegExp[] {
  return [
    // Fargekoder: #0B3D91, #fff, rgb(…), hsl(…), oklch(…), color-mix(…). En # rett etter &
    // eller en bokstav er ingen fargekode, som i HTML-entiteten &#160;.
    /(?<![&\w])#(?:[0-9a-f]{3,4}|[0-9a-f]{6}|[0-9a-f]{8})\b/gi,
    /\b(?:rgba?|hsla?|oklch|oklab|lab|lch|hwb|color|color-mix)\(/gi,
    // Lengder: 13px, 0.5px, 1rem, 0.5em
    /(?:\d*\.)?\d+(?:px|r?em)\b/gi,
    // Fontnavn fra fontstabelen, og font-family i CSS og som React-stil
    ...fonter.map((navn) => new RegExp(`(?<![\\w-])${somRegex(navn)}(?![\\w-])`, 'gi')),
    /font-family|fontFamily/g,
    // Breddeklasser med tall, som border-2, border-t-2, ring-offset-2 og stroke-2. `border`,
    // `border-dashed` og tokenklasser som `border-border` og `ring-accent` gir ikke treff.
    /(?<!\w)(?:border(?:-[xysetrbl])?|outline(?:-offset)?|ring(?:-offset)?|divide-[xy]|underline-offset|decoration|stroke)-\d+(?:\.\d+)?\b/g,
    // Klasser med egne verdier i hakeparentes: p-[13px], bg-[#123456], min-[700px]: og
    // modifikatorer som bg-accent/[0.37]. Treffet er hele klassen, for eksempel `font-[600]`,
    // så den kan stå i `TILLATT`. `/[` krever et klassenavn foran, så et regulært uttrykk som
    // `(/[a-z]/)` ikke gir treff.
    /(?:[\w-]*-|[\w-]+\/)\[[^\]\s]*\]/g,
    // Hakeparenteser uten mellomrom med `:` eller `&`: egne egenskaper som [--gap:1rem] og
    // egne varianter som [&>p]: og [@supports(display:grid)]:. Indekstyper som
    // `{ [navn: string]: string }` har mellomrom og gir ikke treff.
    /\[[^\]\s]*[:&][^\]\s]*\]/g,
  ];
}

/** Hvert treff i `tekst` som ikke står i `TILLATT`, som «linje: treff». */
function finnEgneVerdier(tekst: string, fonter: readonly string[]): string[] {
  const treff: string[] = [];
  const regexer = monstre(fonter);
  for (const [indeks, linje] of tekst.split(/\r?\n/).entries()) {
    for (const regex of regexer) {
      for (const [funnet] of linje.matchAll(regex)) {
        if (!TILLATT.includes(funnet)) {
          treff.push(`${indeks + 1}: ${funnet}`);
        }
      }
    }
  }
  return treff;
}

/** Filene sjekken leser, relativt til `src/` og med `/`. */
function filer(): string[] {
  return readdirSync(SRC, { recursive: true, encoding: 'utf8' })
    .map((fil) => fil.replaceAll('\\', '/'))
    .filter((fil) => ENDELSER.some((endelse) => fil.endsWith(endelse)))
    .filter((fil) => !UNNTATT.includes(fil))
    .sort();
}

const FONTER = fontnavn();

describe('egne verdier under src/', () => {
  it('sjekken leser filene under src/, men ikke unntakene', () => {
    const lest = filer();
    expect(lest).toContain('app/not-found.tsx');
    expect(lest).toContain('api/klient.ts');
    for (const unntak of UNNTATT) {
      expect(existsSync(join(SRC, unntak)), `${unntak} finnes ikke, så unntaket kan fjernes`).toBe(true);
      expect(lest).not.toContain(unntak);
    }
    expect(FONTER.length).toBeGreaterThan(0);
  });

  it('ingen fil har fargekoder, pikselverdier, fontnavn eller klasser med egne verdier', () => {
    const treff = filer().flatMap((fil) =>
      finnEgneVerdier(readFileSync(join(SRC, fil), 'utf8'), FONTER).map((funn) => `src/${fil}:${funn}`),
    );
    expect(treff).toEqual([]);
  });

  it('bare filene under api/ kaller fetch', () => {
    const kallerFetch = (fil: string) => /\bfetch\s*\(/.test(readFileSync(join(SRC, fil), 'utf8'));
    expect(kallerFetch('api/klient.ts')).toBe(true);
    const utenfor = filer().filter((fil) => !fil.startsWith('api/') && kallerFetch(fil));
    expect(utenfor.map((fil) => `src/${fil}`)).toEqual([]);
  });
});

describe('mønstrene', () => {
  it.each([
    '#0B3D91',
    'color: #fff;',
    'rgb(11, 61, 145)',
    'hsl(220 86% 31%)',
    'oklch(0.4 0.1 260)',
    'lab(29% 39 20)',
    'lch(29% 44 27)',
    'hwb(220 4% 43%)',
    'color(srgb 0 0.2 0.6)',
    'color-mix(in srgb, red, blue)',
    '13px',
    'width: 0.5px',
    'gap: 1rem',
    'letter-spacing: 0.5em',
    'border-2',
    'border-t-2',
    'border-x-2',
    'outline-2',
    'outline-offset-2',
    'ring-2',
    'ring-offset-2',
    'divide-x-2',
    'underline-offset-2',
    'decoration-2',
    'stroke-2',
    'Arial',
    '"Segoe UI"',
    'system-ui',
    '-apple-system',
    'sans-serif',
    'font-family: x',
    'style={{ fontFamily: x }}',
    'className="p-[13px]"',
    'bg-[#123456]',
    'min-[700px]:block',
    'font-[600]',
    'bg-accent/[0.37]',
    '[mask-type:alpha]',
    '[&>p]:mt-heading-gap',
    '[--gap:1rem]',
    '[@supports(display:grid)]:grid',
    '[.dark_&]:x',
  ])('finner %s', (tekst) => {
    expect(finnEgneVerdier(tekst, FONTER)).not.toEqual([]);
  });

  it.each([
    'className="mx-auto max-w-content-max-width px-page-x-mobile desktop:px-page-x"',
    'min-h-target-min desktop:min-h-target-min-inline',
    'font-sans text-status-headline',
    'border border-border border-status-grey-border border-dashed',
    'ring-accent stroke-accent',
    '&#160;',
    'rader[0]',
    "components['schemas']['Uke']",
    '{ [navn: string]: string }',
    "'http://127.0.0.1:8000'",
    '«uke 42, 2026»',
  ])('godtar %s', (tekst) => {
    expect(finnEgneVerdier(tekst, FONTER)).toEqual([]);
  });
});

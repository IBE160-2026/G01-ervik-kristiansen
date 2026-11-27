/**
 * `formatLus` og `formatUke` mot de samme vektorene som kjernen (AD-6), i
 * `backend/tests/data/format.json`. Nøkkelen `grense` har ingen motpart i frontend.
 */
import { readFileSync } from 'node:fs';

import { describe, expect, it } from 'vitest';

// Importen går gjennom aliaset `@/` i vitest.config.ts.
import { formatLus, formatUke } from '@/lib/format';

type Vektorer = {
  lus: { verdi: number; tekst: string }[];
  uke: { ar: number; uke: number; tekst: string }[];
};

const vektorer = JSON.parse(
  readFileSync(new URL('../../backend/tests/data/format.json', import.meta.url), 'utf8'),
) as Vektorer;

describe('vektorene', () => {
  it('har lusetall og uker', () => {
    expect(vektorer.lus.length).toBeGreaterThan(0);
    expect(vektorer.uke.length).toBeGreaterThan(0);
  });
});

describe('formatLus', () => {
  it.each(vektorer.lus)('skriver $verdi som «$tekst»', ({ verdi, tekst }) => {
    expect(formatLus(verdi)).toBe(tekst);
  });

  it('skriver aldri null med minustegn', () => {
    expect(formatLus(-0)).toBe('0,00');
    expect(formatLus(-0.001)).toBe('0,00');
  });
});

describe('formatUke', () => {
  it.each(vektorer.uke)('skriver år $ar uke $uke som «$tekst»', ({ ar, uke, tekst }) => {
    expect(formatUke({ ar, uke })).toBe(tekst);
  });
});

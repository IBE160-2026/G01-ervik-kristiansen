/**
 * `@theme` i `src/app/globals.css` skal ha nøyaktig tokenene i frontmatteren i DESIGN.md,
 * hvert én gang og med samme verdi. DESIGN.md er fasit. Frontmatteren leses med en liten
 * leser for den delen av YAML som DESIGN.md bruker, så testen trenger ingen YAML-pakke.
 */
import { readFileSync } from 'node:fs';

import { describe, expect, it } from 'vitest';

const DESIGN_MD = new URL('../../_bmad-output/planning-artifacts/ux-designs/ux-Marin-2026-11-11/DESIGN.md', import.meta.url);
const GLOBALS_CSS = new URL('../src/app/globals.css', import.meta.url);

/** Seksjonene i frontmatteren som blir tokens i `@theme`. */
const SEKSJONER = ['colors', 'typography', 'rounded', 'spacing'] as const;

/** Egenskapene i en typografirolle som blir egne variabler etter `--text-<rolle>`. */
const TYPOGRAFI_SUFFIKS: Readonly<Record<string, string>> = {
  fontWeight: '--font-weight',
  letterSpacing: '--letter-spacing',
  lineHeight: '--line-height',
};

type Kart = { [navn: string]: string | Kart };
type Deklarasjon = { navn: string; verdi: string };

function medLf(tekst: string): string {
  return tekst.replace(/\r\n/g, '\n');
}

/**
 * Leser seksjonene `SEKSJONER` i frontmatteren: mapper med innrykk og verdier med eller uten
 * enkle anførselstegn. `#` starter en kommentar, unntatt inne i anførselstegn. Andre seksjoner
 * hoppes over. Former leseren ikke kjenner, gir en feil i stedet for en feil verdi.
 */
function lesFrontmatter(markdown: string): Kart {
  const frontmatter = /^---\n([\s\S]*?)\n---\n/.exec(medLf(markdown))?.[1];
  if (frontmatter === undefined) {
    throw new Error('fant ikke frontmatteren');
  }
  const rot: Kart = {};
  const stabel: { innrykk: number; kart: Kart }[] = [{ innrykk: -1, kart: rot }];
  let iSeksjon = false;
  for (const [indeks, linje] of frontmatter.split('\n').entries()) {
    const linjenr = indeks + 2; // Linje 1 er `---`.
    const innhold = linje.trimStart();
    if (innhold === '' || innhold.startsWith('#')) {
      continue;
    }
    const innrykk = linje.length - innhold.length;
    if (innrykk === 0) {
      iSeksjon = (SEKSJONER as readonly string[]).includes(innhold.split(':')[0] ?? '');
    }
    if (!iSeksjon) {
      continue;
    }
    if (linje.slice(0, innrykk).includes('\t')) {
      throw new Error(`linje ${linjenr}: innrykk med tabulator`);
    }
    const nokkel = /^([\w-]+):(?:\s+(.*))?$/.exec(innhold);
    if (!nokkel?.[1]) {
      throw new Error(`linje ${linjenr}: forventet «nøkkel: verdi», fant ${innhold}`);
    }
    const navn = nokkel[1];
    const verdi = lesVerdi(nokkel[2] ?? '', linjenr);
    while ((stabel.at(-1)?.innrykk ?? -1) >= innrykk) {
      stabel.pop();
    }
    const forelder = stabel.at(-1)?.kart;
    if (forelder === undefined) {
      throw new Error(`linje ${linjenr}: uventet innrykk`);
    }
    if (navn in forelder) {
      throw new Error(`linje ${linjenr}: ${navn} står to ganger`);
    }
    if (verdi === null) {
      const barn: Kart = {};
      forelder[navn] = barn;
      stabel.push({ innrykk, kart: barn });
    } else {
      forelder[navn] = verdi;
    }
  }
  return rot;
}

/** Verdien etter kolon, uten kommentar. `null` betyr at en ny mappe starter. */
function lesVerdi(raa: string, linjenr: number): string | null {
  if (raa === '' || raa.startsWith('#')) {
    return null;
  }
  if (raa.startsWith("'")) {
    // Enkle anførselstegn: `''` er et anførselstegn i verdien, og `#` er vanlig tekst.
    let verdi = '';
    let fra = 1;
    for (;;) {
      const slutt = raa.indexOf("'", fra);
      if (slutt === -1) {
        throw new Error(`linje ${linjenr}: mangler avsluttende anførselstegn`);
      }
      verdi += raa.slice(fra, slutt);
      if (raa[slutt + 1] === "'") {
        verdi += "'";
        fra = slutt + 2;
        continue;
      }
      const rest = raa.slice(slutt + 1).trim();
      if (rest !== '' && !rest.startsWith('#')) {
        throw new Error(`linje ${linjenr}: tekst etter anførselstegnet: ${rest}`);
      }
      return verdi;
    }
  }
  if (/^["[{|>&*!%@`]/.test(raa)) {
    throw new Error(`linje ${linjenr}: leseren støtter ikke verdien ${raa}`);
  }
  const kommentar = raa.search(/\s#/);
  return (kommentar === -1 ? raa : raa.slice(0, kommentar)).trim();
}

function seksjon(design: Kart, navn: string): Kart {
  const verdi = design[navn];
  if (typeof verdi !== 'object') {
    throw new Error(`DESIGN.md mangler seksjonen ${navn}`);
  }
  return verdi;
}

function tekstverdi(verdi: string | Kart, sti: string): string {
  if (typeof verdi !== 'string') {
    throw new Error(`${sti} skal være en verdi, ikke en mappe`);
  }
  return verdi;
}

/** `fontFamily` i hver typografirolle, med rollen som nøkkel. */
function fontFamilier(design: Kart): Map<string, string | undefined> {
  const familier = new Map<string, string | undefined>();
  for (const [rolle, egenskaper] of Object.entries(seksjon(design, 'typography'))) {
    if (typeof egenskaper === 'string') {
      throw new Error(`typography.${rolle} skal være en mappe`);
    }
    const familie = egenskaper.fontFamily;
    familier.set(rolle, familie === undefined ? undefined : tekstverdi(familie, `typography.${rolle}.fontFamily`));
  }
  return familier;
}

/** Variablene `@theme` skal ha, regnet ut fra frontmatteren (Design Notes i specen). */
function forventedeTokens(design: Kart): Map<string, string> {
  const tokens = new Map<string, string>();
  const leggTil = (navn: string, verdi: string) => {
    if (tokens.has(navn)) {
      throw new Error(`DESIGN.md gir ${navn} to ganger`);
    }
    tokens.set(navn, verdi);
  };

  leggTil('--*', 'initial');
  leggTil('--breakpoint-desktop', '600px');
  const familie = [...fontFamilier(design).values()][0];
  if (familie === undefined) {
    throw new Error('typography mangler fontFamily');
  }
  leggTil('--font-sans', familie);

  for (const [navn, verdi] of Object.entries(seksjon(design, 'colors'))) {
    leggTil(`--color-${navn}`, tekstverdi(verdi, `colors.${navn}`));
  }
  for (const [rolle, egenskaper] of Object.entries(seksjon(design, 'typography'))) {
    if (typeof egenskaper === 'string') {
      throw new Error(`typography.${rolle} skal være en mappe`);
    }
    if (egenskaper.fontSize === undefined) {
      throw new Error(`typography.${rolle} mangler fontSize`);
    }
    for (const [egenskap, verdi] of Object.entries(egenskaper)) {
      const tekst = tekstverdi(verdi, `typography.${rolle}.${egenskap}`);
      if (egenskap === 'fontFamily') {
        continue; // Blir `--font-sans`, sjekket for seg.
      }
      if (egenskap === 'fontSize') {
        leggTil(`--text-${rolle}`, tekst);
        continue;
      }
      const suffiks = TYPOGRAFI_SUFFIKS[egenskap];
      if (suffiks === undefined) {
        throw new Error(`typography.${rolle}.${egenskap} har ingen variabel i @theme`);
      }
      leggTil(`--text-${rolle}${suffiks}`, tekst);
    }
  }
  for (const [navn, verdi] of Object.entries(seksjon(design, 'rounded'))) {
    leggTil(`--radius-${navn === 'DEFAULT' ? 'default' : navn}`, tekstverdi(verdi, `rounded.${navn}`));
  }
  for (const [navn, verdi] of Object.entries(seksjon(design, 'spacing'))) {
    leggTil(`--spacing-${navn}`, tekstverdi(verdi, `spacing.${navn}`));
  }
  return tokens;
}

/**
 * Den ene `@theme`-blokka: hodet foran `{`, som `@theme static`, og deklarasjonene i
 * rekkefølge, uten kommentarer.
 */
function lesTheme(css: string): { hode: string; deklarasjoner: Deklarasjon[] } {
  const utenKommentarer = css.replace(/\/\*[\s\S]*?\*\//g, '');
  const starter = [...utenKommentarer.matchAll(/@theme\b[^{;]*\{/g)];
  const start = starter[0];
  if (starter.length !== 1 || start === undefined) {
    throw new Error(`globals.css skal ha én @theme-blokk, men har ${starter.length}`);
  }
  const fra = start.index + start[0].length;
  const til = utenKommentarer.indexOf('}', fra);
  if (til === -1) {
    throw new Error('@theme-blokka er ikke lukket');
  }
  const blokk = utenKommentarer.slice(fra, til);
  if (blokk.includes('{')) {
    throw new Error('@theme-blokka har en blokk inni seg');
  }
  const deklarasjoner = blokk
    .split(';')
    .map((deklarasjon) => deklarasjon.trim())
    .filter((deklarasjon) => deklarasjon !== '')
    .map((deklarasjon) => {
      const kolon = deklarasjon.indexOf(':');
      if (kolon === -1) {
        throw new Error(`@theme har en linje uten kolon: ${deklarasjon}`);
      }
      return { navn: deklarasjon.slice(0, kolon).trim(), verdi: deklarasjon.slice(kolon + 1).trim() };
    });
  return { hode: start[0].slice(0, -1).trim(), deklarasjoner };
}

/** Hvert token som har en annen verdi, mangler, står flere ganger eller er ekstra i `@theme`. */
function finnAvvik(forventet: ReadonlyMap<string, string>, faktisk: readonly Deklarasjon[]): string[] {
  const avvik: string[] = [];
  const verdier = new Map<string, string[]>();
  for (const { navn, verdi } of faktisk) {
    verdier.set(navn, [...(verdier.get(navn) ?? []), verdi]);
  }
  for (const [navn, funnet] of verdier) {
    if (funnet.length > 1) {
      avvik.push(`${navn} står ${funnet.length} ganger i @theme`);
    }
    if (!forventet.has(navn)) {
      avvik.push(`${navn} står i @theme, men ikke i DESIGN.md`);
    }
  }
  for (const [navn, verdi] of forventet) {
    const funnet = verdier.get(navn);
    if (funnet === undefined) {
      avvik.push(`${navn} mangler i @theme (DESIGN.md: ${verdi})`);
    } else if (funnet.some((f) => f !== verdi)) {
      avvik.push(`${navn} er ${funnet.join(' og ')} i @theme, men ${verdi} i DESIGN.md`);
    }
  }
  return avvik;
}

const design = lesFrontmatter(readFileSync(DESIGN_MD, 'utf8'));
const { hode, deklarasjoner: theme } = lesTheme(readFileSync(GLOBALS_CSS, 'utf8'));

describe('tokenene i @theme', () => {
  it('DESIGN.md har farger, typografi, hjørner og avstander', () => {
    for (const navn of SEKSJONER) {
      expect(Object.keys(seksjon(design, navn)).length, `${navn} er tom`).toBeGreaterThan(0);
    }
  });

  it('alle typografirollene har samme fontFamily', () => {
    const familier = fontFamilier(design);
    const forste = [...familier.values()][0];
    expect(forste).toBeTruthy();
    const avvik = [...familier].filter(([, familie]) => familie !== forste).map(([rolle, familie]) => `typography.${rolle}: ${familie}`);
    expect(avvik).toEqual([]);
  });

  it('blokka er @theme static, så alle variablene skrives til CSS-en', () => {
    expect(hode).toBe('@theme static');
  });

  it('@theme starter med --*: initial', () => {
    expect(theme[0]).toEqual({ navn: '--*', verdi: 'initial' });
  });

  it('@theme har tokenene fra DESIGN.md, hvert én gang og med samme verdi', () => {
    const forventet = forventedeTokens(design);
    // `--*`, bruddpunktet og fonten står fast i testen. Resten kommer fra DESIGN.md, og en tom
    // liste på en av sidene skal ikke kunne gi en grønn test.
    expect(forventet.size).toBeGreaterThan(3);
    expect(theme.length).toBeGreaterThan(1);
    expect(finnAvvik(forventet, theme)).toEqual([]);
  });

  it('bruddpunktet desktop er det eneste --breakpoint-*', () => {
    expect(theme.filter(({ navn }) => navn.startsWith('--breakpoint-'))).toEqual([{ navn: '--breakpoint-desktop', verdi: '600px' }]);
  });
});

describe('leseren av frontmatteren', () => {
  it('leser verdier med og uten anførselstegn og hopper over kommentarer', () => {
    const tekst = [
      '---',
      'title: "Hoppes over"',
      'sources:',
      '  - hoppes/over.md',
      'colors:',
      '  # en kommentar',
      "  accent: '#0B3D91'   # 10,0:1",
      "  sitat: 'it''s'",
      'typography:',
      '  body:',
      `    fontFamily: 'system-ui, "Segoe UI", sans-serif'`,
      '    fontSize: 18px     # kommentar',
      "    lineHeight: '1.55'",
      'rounded:',
      '  DEFAULT: 6px',
      'components:',
      "  bar: '{colors.accent}'",
      '---',
      '',
    ].join('\n');
    expect(lesFrontmatter(tekst)).toEqual({
      colors: { accent: '#0B3D91', sitat: "it's" },
      typography: { body: { fontFamily: 'system-ui, "Segoe UI", sans-serif', fontSize: '18px', lineHeight: '1.55' } },
      rounded: { DEFAULT: '6px' },
    });
  });

  it('feiler på former den ikke kjenner, i stedet for å gi en feil verdi', () => {
    expect(() => lesFrontmatter('---\ncolors:\n  accent: "#0B3D91"\n---\n')).toThrow(/linje 3/);
    expect(() => lesFrontmatter('---\nspacing:\n  - 4px\n---\n')).toThrow(/linje 3/);
  });

  it('feiler på en nøkkel som står to ganger', () => {
    expect(() => lesFrontmatter('---\nspacing:\n  page-x: 32px\n  page-x: 16px\n---\n')).toThrow(/linje 4: page-x står to ganger/);
  });

  it('feiler på tekst etter det avsluttende anførselstegnet', () => {
    expect(() => lesFrontmatter("---\ncolors:\n  accent: '#0B3D91' ekstra\n---\n")).toThrow(/linje 3: tekst etter anførselstegnet/);
  });

  it('feiler når det avsluttende anførselstegnet mangler', () => {
    expect(() => lesFrontmatter("---\ncolors:\n  accent: '#0B3D91\n---\n")).toThrow(/linje 3: mangler avsluttende anførselstegn/);
  });
});

describe('leseren av @theme', () => {
  it('feiler på to @theme-blokker', () => {
    expect(() => lesTheme('@theme static {\n  --*: initial;\n}\n@theme {\n  --color-x: #000000;\n}\n')).toThrow(/én @theme-blokk, men har 2/);
  });

  it('feiler på en deklarasjon uten kolon', () => {
    expect(() => lesTheme('@theme static {\n  --*: initial;\n  --color-x #000000;\n}\n')).toThrow(/uten kolon: --color-x #000000/);
  });
});

describe('sammenligningen', () => {
  const forventet = new Map([
    ['--*', 'initial'],
    ['--color-accent', '#0B3D91'],
    ['--spacing-page-x', '32px'],
  ]);
  const riktig: Deklarasjon[] = [
    { navn: '--*', verdi: 'initial' },
    { navn: '--color-accent', verdi: '#0B3D91' },
    { navn: '--spacing-page-x', verdi: '32px' },
  ];

  it('godtar like tokens', () => {
    expect(finnAvvik(forventet, riktig)).toEqual([]);
  });

  it('nevner tokenet som har en annen verdi', () => {
    const avvik = finnAvvik(forventet, [riktig[0]!, { navn: '--color-accent', verdi: '#0B3D92' }, riktig[2]!]);
    expect(avvik).toEqual(['--color-accent er #0B3D92 i @theme, men #0B3D91 i DESIGN.md']);
  });

  it('nevner tokenet som mangler', () => {
    expect(finnAvvik(forventet, [riktig[0]!, riktig[2]!])).toEqual(['--color-accent mangler i @theme (DESIGN.md: #0B3D91)']);
  });

  it('nevner tokenet som står to ganger', () => {
    expect(finnAvvik(forventet, [...riktig, riktig[2]!])).toEqual(['--spacing-page-x står 2 ganger i @theme']);
  });

  it('nevner tokenet som er ekstra', () => {
    expect(finnAvvik(forventet, [...riktig, { navn: '--spacing-ekstra', verdi: '4px' }])).toEqual([
      '--spacing-ekstra står i @theme, men ikke i DESIGN.md',
    ]);
  });
});

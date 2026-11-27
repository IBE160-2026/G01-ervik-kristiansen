/**
 * `src/api/schema.ts` skal være lik det `npm run typer` lager av `backend/openapi.json` nå
 * (AD-3). Mønsteret er `test_openapi_json_er_lik_skjemaet_appen_lager` i backend.
 */
import { execFileSync } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

import { expect, it } from 'vitest';

const frontend = fileURLToPath(new URL('..', import.meta.url));
const cli = join(frontend, 'node_modules', 'openapi-typescript', 'bin', 'cli.js');

/** CRLF gjøres om til LF, så testen tåler `core.autocrlf` på Windows. */
function medLf(tekst: string): string {
  return tekst.replace(/\r\n/g, '\n');
}

it('npm run typer er samme kommando som testen kjører', () => {
  const pakke = JSON.parse(readFileSync(join(frontend, 'package.json'), 'utf8')) as { scripts?: Record<string, string> };
  expect(pakke.scripts?.typer).toBe('openapi-typescript ../backend/openapi.json -o src/api/schema.ts');
});

it('schema.ts er lik det npm run typer lager av openapi.json', { timeout: 60_000 }, () => {
  const mappe = mkdtempSync(join(tmpdir(), 'marin-schema-'));
  try {
    const utfil = join(mappe, 'schema.ts');
    // Samme kommando som `npm run typer`, med samme arbeidsmappe og inndata, men uten skall
    // og til en midlertidig fil.
    execFileSync(process.execPath, [cli, '../backend/openapi.json', '-o', utfil], { cwd: frontend, stdio: 'pipe' });
    const generert = medLf(readFileSync(utfil, 'utf8'));
    const committet = medLf(readFileSync(join(frontend, 'src', 'api', 'schema.ts'), 'utf8'));
    expect(generert.length).toBeGreaterThan(0);
    expect(committet, 'schema.ts er utdatert: kjør npm run typer i frontend/').toBe(generert);
  } finally {
    rmSync(mappe, { recursive: true, force: true });
  }
});

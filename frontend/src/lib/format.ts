/**
 * Tekstformat for lusetall og uker (AD-6, NFR5), som `format_lus` og `format_uke` i
 * `backend/src/marin/kjerne/formatering.py`. Begge testes mot vektorene i
 * `backend/tests/data/format.json`. Grenser og uker i statustekster skriver kjernen selv.
 */
import type { Uke } from '@/api/typer';

/**
 * Lusetall med 2 desimaler og desimalkomma, for eksempel «0,06» og «0,50». Kjernen har
 * allerede avrundet lusetallene til høyst 2 desimaler, så `toFixed` endrer ikke verdien. Null
 * har aldri minustegn, som i kjernen.
 */
export function formatLus(verdi: number): string {
  const tekst = verdi.toFixed(2);
  return (tekst === '-0.00' ? '0.00' : tekst).replace('.', ',');
}

/** ISO-uke med år, for eksempel «uke 42, 2026». */
export function formatUke(uke: Uke): string {
  return `uke ${uke.uke}, ${uke.ar}`;
}

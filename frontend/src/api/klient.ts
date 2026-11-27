/**
 * Den eneste veien til API-et (AD-3). Alle kall går gjennom `hentJson`, og ingen kode utenfor
 * `src/api/` bruker `fetch`. Kallene per rute lages i Story 2.4, 2.7 og 2.9.
 */

/**
 * Starten på adressen til API-et. I utvikling kjører API-et for seg på port 8000, og CORS
 * tillater bare opphavet `http://localhost:3000`, der `npm run dev` kjører frontenden. I bygget
 * kommer API-et fra samme opphav som sidene, både lokalt fra FastAPI og på Vercel, så stien
 * brukes alene.
 */
export function apiBase(): string {
  return process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:8000' : '';
}

/**
 * Et svar fra API-et med en annen status enn 2xx. `detail` er teksten i FastAPIs `{detail}`,
 * for eksempel «Fant ikke anlegget.» ved 404. Den er `null` når `detail` ikke er en streng,
 * som listen ved 422, eller når kroppen ikke er JSON.
 */
export class ApiFeil extends Error {
  override readonly name = 'ApiFeil';

  constructor(
    readonly status: number,
    readonly detail: string | null,
  ) {
    super(detail ?? `API-et svarte ${status}`);
  }
}

/**
 * Henter `sti` fra API-et og gir JSON-svaret ved 2xx. Ved andre statuser kastes `ApiFeil`.
 * Nettverksfeil og avbrudd fra `signal` slipper uendret gjennom, også når de kommer mens
 * kroppen leses, så kallet kan skille et avbrutt kall fra en feil.
 */
export async function hentJson<T>(sti: string, signal?: AbortSignal): Promise<T> {
  const svar = await fetch(`${apiBase()}${sti}`, { signal });
  if (svar.ok) {
    return (await svar.json()) as T;
  }
  throw new ApiFeil(svar.status, await lesDetail(svar));
}

/** Teksten i `detail` når kroppen er JSON med `detail` som streng, ellers `null`. */
async function lesDetail(svar: Response): Promise<string | null> {
  let kropp: unknown;
  try {
    kropp = await svar.json();
  } catch (feil) {
    // Bare en kropp som ikke er JSON, gir `null`. Avbrudd og nettverksfeil sendes videre.
    if (feil instanceof SyntaxError) {
      return null;
    }
    throw feil;
  }
  if (typeof kropp === 'object' && kropp !== null && 'detail' in kropp && typeof kropp.detail === 'string') {
    return kropp.detail;
  }
  return null;
}

/**
 * API-basen og `hentJson` (AD-3). `fetch` byttes ut med `vi.stubGlobal`, og `NODE_ENV` med
 * `vi.stubEnv`, så testene sender aldri noe over nett.
 */
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { ApiFeil, apiBase, hentJson } from '../src/api/klient';

const STI = '/api/anlegg?q=x';

// Vitest setter bare NODE_ENV når den mangler, så en NODE_ENV fra skallet ville styrt API-basen.
beforeEach(() => {
  vi.stubEnv('NODE_ENV', 'test');
});

afterEach(() => {
  vi.unstubAllGlobals();
  vi.unstubAllEnvs();
});

/** Bytter ut `fetch` med en som gir `svar`, og gir den tilbake så kallene kan sjekkes. */
function stubFetch(svar: Response) {
  const falskFetch = vi.fn<typeof fetch>().mockResolvedValue(svar);
  vi.stubGlobal('fetch', falskFetch);
  return falskFetch;
}

function jsonSvar(status: number, kropp: unknown): Response {
  return new Response(JSON.stringify(kropp), { status, headers: { 'content-type': 'application/json' } });
}

/** Gir feilen som løftet avvises med, eller feiler testen hvis det ikke avvises. */
async function avvisning(lofte: Promise<unknown>): Promise<unknown> {
  try {
    await lofte;
  } catch (feil) {
    return feil;
  }
  throw new Error('kallet skulle ha feilet');
}

describe('apiBase', () => {
  it('er tom i bygget, så stien går til samme opphav', () => {
    vi.stubEnv('NODE_ENV', 'production');
    expect(apiBase()).toBe('');
  });

  it('er tom i testene', () => {
    vi.stubEnv('NODE_ENV', 'test');
    expect(apiBase()).toBe('');
  });

  it('er API-et på port 8000 i utvikling', () => {
    vi.stubEnv('NODE_ENV', 'development');
    expect(apiBase()).toBe('http://127.0.0.1:8000');
  });
});

describe('hentJson ved 2xx', () => {
  const treff = [{ lokalitetsnr: 12345, navn: 'Testanlegget', kommune: 'Hitra', fylke: 'Trøndelag' }];

  it('kaller stien alene i bygget og gir JSON-svaret', async () => {
    vi.stubEnv('NODE_ENV', 'production');
    const falskFetch = stubFetch(jsonSvar(200, treff));
    await expect(hentJson(STI)).resolves.toEqual(treff);
    expect(falskFetch).toHaveBeenCalledTimes(1);
    expect(falskFetch).toHaveBeenCalledWith(STI, { signal: undefined });
  });

  it('kaller API-et på port 8000 i utvikling', async () => {
    vi.stubEnv('NODE_ENV', 'development');
    const falskFetch = stubFetch(jsonSvar(200, treff));
    await expect(hentJson(STI)).resolves.toEqual(treff);
    expect(falskFetch).toHaveBeenCalledWith(`http://127.0.0.1:8000${STI}`, { signal: undefined });
  });

  it('gir også JSON-svaret ved andre 2xx-statuser', async () => {
    stubFetch(jsonSvar(201, { ok: true }));
    await expect(hentJson(STI)).resolves.toEqual({ ok: true });
  });

  it('sender signalet videre til fetch', async () => {
    const falskFetch = stubFetch(jsonSvar(200, []));
    const signal = new AbortController().signal;
    await hentJson(STI, signal);
    expect(falskFetch).toHaveBeenCalledWith(STI, { signal });
  });
});

describe('hentJson ved andre statuser', () => {
  it('kaster ApiFeil med 404 og teksten i detail', async () => {
    stubFetch(jsonSvar(404, { detail: 'Fant ikke anlegget.' }));
    const feil = await avvisning(hentJson(STI));
    expect(feil).toBeInstanceOf(ApiFeil);
    expect(feil).toBeInstanceOf(Error);
    expect(feil).toMatchObject({ name: 'ApiFeil', status: 404, detail: 'Fant ikke anlegget.', message: 'Fant ikke anlegget.' });
  });

  it('kaster ApiFeil med 422 og detail null når detail er en liste', async () => {
    stubFetch(jsonSvar(422, { detail: [{ loc: ['query', 'uke'], msg: 'Feil uke', type: 'value_error' }] }));
    const feil = await avvisning(hentJson(STI));
    expect(feil).toBeInstanceOf(ApiFeil);
    expect(feil).toMatchObject({ status: 422, detail: null, message: 'API-et svarte 422' });
  });

  it.each([
    ['tekst som ikke er JSON', 500, new Response('Internal Server Error', { status: 500 })],
    ['en HTML-side', 502, new Response('<!doctype html><title>Bad Gateway</title>', { status: 502 })],
    ['tom', 503, new Response(null, { status: 503 })],
    ['JSON uten detail', 500, jsonSvar(500, { feil: 'noe' })],
    ['JSON der detail er et tall', 500, jsonSvar(500, { detail: 7 })],
    ['JSON som er null', 500, jsonSvar(500, null)],
  ])('kaster ApiFeil med statusen og detail null når kroppen er %s', async (_navn, status, svar) => {
    stubFetch(svar);
    const feil = await avvisning(hentJson(STI));
    expect(feil).toBeInstanceOf(ApiFeil);
    expect(feil).toMatchObject({ status, detail: null, message: `API-et svarte ${status}` });
  });
});

describe('hentJson ved nettverksfeil og avbrudd', () => {
  it('slipper nettverksfeil uendret gjennom', async () => {
    const nettverksfeil = new TypeError('fetch failed');
    vi.stubGlobal('fetch', vi.fn<typeof fetch>().mockRejectedValue(nettverksfeil));
    expect(await avvisning(hentJson(STI))).toBe(nettverksfeil);
  });

  it('slipper avbrudd fra signalet uendret gjennom', async () => {
    // Som fetch i nettleseren: kallet avvises med grunnen til avbruddet.
    vi.stubGlobal(
      'fetch',
      vi.fn<typeof fetch>(
        (_adresse, init) =>
          new Promise((_los, avvis) => {
            init?.signal?.addEventListener('abort', () => avvis(init.signal?.reason));
          }),
      ),
    );
    const kontroller = new AbortController();
    const lofte = avvisning(hentJson(STI, kontroller.signal));
    kontroller.abort();
    const feil = await lofte;
    expect(feil).toBe(kontroller.signal.reason);
    expect(feil).toBeInstanceOf(DOMException);
    expect(feil).toMatchObject({ name: 'AbortError' });
  });

  it('slipper avbrudd uendret gjennom når det kommer mens feilsvaret leses', async () => {
    const avbrudd = new DOMException('Avbrutt', 'AbortError');
    const svar = new Response(null, { status: 500 });
    vi.spyOn(svar, 'json').mockRejectedValue(avbrudd);
    stubFetch(svar);
    expect(await avvisning(hentJson(STI))).toBe(avbrudd);
  });
});

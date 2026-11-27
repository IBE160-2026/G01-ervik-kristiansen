/**
 * Faste tekster i grensesnittet (AD-2). Tekster som avhenger av data eller regelutfall,
 * lager kjernen, og frontend viser dem uendret fra API-et.
 */
export const tekster = {
  /** Navnet på appen, brukt i `<title>`. */
  appnavn: 'Marin',
  /** 404-siden for stier som ikke finnes (`app/not-found.tsx`, `out/404.html` i bygget). */
  ikkeFunnet: {
    overskrift: 'Fant ikke siden.',
    tilForsiden: 'Gå til forsiden',
  },
} as const;

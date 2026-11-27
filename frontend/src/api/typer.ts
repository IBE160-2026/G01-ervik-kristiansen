/**
 * Typenavnene for svarene fra API-et, ett per skjema i `backend/openapi.json`. De hentes fra
 * `schema.ts`, som `npm run typer` lager, så komponentene slipper å skrive
 * `components['schemas']['…']`.
 */
import type { components } from './schema';

type Skjemaer = components['schemas'];

export type AnleggInfo = Skjemaer['AnleggInfo'];
export type Anleggsvar = Skjemaer['Anleggsvar'];
export type Arsak = Skjemaer['Arsak'];
export type Detaljsvar = Skjemaer['Detaljsvar'];
export type EstimertUke = Skjemaer['EstimertUke'];
export type Farge = Skjemaer['Farge'];
export type Graf = Skjemaer['Graf'];
export type Grafpunkt = Skjemaer['Grafpunkt'];
export type Kryssing = Skjemaer['Kryssing'];
export type Status = Skjemaer['Status'];
export type Tabellrad = Skjemaer['Tabellrad'];
export type Uke = Skjemaer['Uke'];

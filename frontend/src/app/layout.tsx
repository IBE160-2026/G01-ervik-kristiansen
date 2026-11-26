import type { Metadata } from 'next';
import type { ReactNode } from 'react';

import { tekster } from '@/tekster';

import './globals.css';

export const metadata: Metadata = {
  title: tekster.appnavn,
};

/** Rotlayouten: norsk språk, og grunnreglene for font, farger, lenker og fokus fra `globals.css`. */
export default function RotLayout({ children }: Readonly<{ children: ReactNode }>) {
  return (
    <html lang="nb">
      <body>{children}</body>
    </html>
  );
}

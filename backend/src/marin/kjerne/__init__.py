"""Kjernen i Marin: regler, ISO-uker, avrunding og tekster som rene funksjoner.

Kjernen importerer bare standardbiblioteket og seg selv, gjør ingen I/O og leser
aldri klokka (AD-1, AD-5). Testen i tests/test_kjerne_importer.py sjekker importene,
bruk av round og avlesning av klokka. At kjernen ikke gjør I/O, sjekkes ikke automatisk.
"""

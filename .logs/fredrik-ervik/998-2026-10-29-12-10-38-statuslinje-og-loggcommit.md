# Statuslinje og loggcommit

## 2026-10-29 kl. 12:10 — Fredrik Ervik

### Oppgave
To ting i samme økt: (1) `/statusline` — sette opp Claude Code-statuslinja ut fra PS1-oppsettet i skallet. (2) Lage en loggfil for økten og sørge for at sesjonslogg-skillen alltid committer loggfila etter at den er skrevet, og bare loggfilene, slik at loggene ikke kommer ut av sync.

### Plan
- Statuslinje: delegert til statusline-setup-agenten.
- Loggcommit: sjekke `.claude/skills/sesjonslogg/SKILL.md` for et eksisterende krav før noe legges inn.
- Skrive denne loggen og committe den med en commit som er begrenset til loggfilene.

### Resultat
- Statuslinje: ikke satt opp. Det finnes ingen PS1 å kopiere (Windows/PowerShell; `.bashrc`, `.bash_profile`, `.zshrc` og `.profile` finnes ikke). `~/.claude/settings.json` er uendret.
- Loggcommit: kravet finnes allerede i `.claude/skills/sesjonslogg/SKILL.md`, seksjonen «Commit loggfila (alltid)», lagt inn i commit c48ff36. Seksjonen sier:
  - loggfila skal committes umiddelbart etter at den er skrevet, uten å spørre om lov
  - commiten skal bare inneholde loggfila og `issues.md`, og den er path-begrenset (`git commit -- <filer>`) slik at filer som allerede er staget ikke blir med
  - innholdet skal kontrolleres med `git show --stat HEAD`
  - ingen push uten at brukeren ber om det

  `CLAUDE.md` viser også til at skillen committer loggfila. Skillen er derfor ikke endret, for å unngå et duplisert krav.
- Kravet ble fulgt i praksis i denne økten: den forrige loggcommiten (9343d06) inneholdt bare de to loggfilene, selv om omtrent 200 andre filer lå i staging-området.

### Åpne punkter
- Statuslinje: velg mellom å bygge en fra bunnen eller å bruke en eksisterende prompt-konfigurasjon (PowerShell `$PROFILE`, Oh My Posh, Starship, Git Bash/WSL).

## 2026-10-29 kl. 16:44 — Fredrik Ervik

### Oppgave
Fredrik spurte hvordan loggene i `.logs/` kommer inn på GitHub, og ba deretter om pull og push.

### Plan
- Forklare at sesjonslogg-skillen bare committer lokalt, og at push gjøres av brukeren (`CLAUDE.md`).
- Sjekke status mot GitHub, stashe stagede filer, kjøre `git pull --rebase` og pushe.

### Resultat
- Loggfilene var committet, men lå ikke på GitHub. Lokal `main` var 10 commits foran og 2 bak `origin/main`.
- De 2 commitene på GitHub var Fredriks egne README-endringer (6d26564, cfb8ae8). Den ukommitterte README-endringen lokalt var identisk med dem og førte ikke til konflikt.
- Stagede BMAD-filer ble stashet. `git pull --rebase origin main` rebaserte de 10 commitene uten konflikt, og `git push` sendte dem til GitHub (`cfb8ae8..1b5427f`). Stashen ble lagt tilbake etterpå.
- Pushen tok også med briefen satt til final og dataanalysen i addendumet, i tillegg til loggcommitene.
- Rebasen ga de 10 commitene nye hasher. Hashene som står i tidligere loggseksjoner, gjelder bare lokalt fra før rebasen. På GitHub er de: f52caec → e7bb92c (brief final), bb2cc01 → af18a77 (dataanalyse i addendum), 9343d06 → b1715e9 (loggcommit).
- Loggene ligger nå på GitHub under `.logs/fredrik-ervik/`.

### Åpne punkter
Ingen.

# oa-autograding

Kontroly cvičení pro [classroom50](https://github.com/foundation50/classroom50)
s českou zpětnou vazbou pro žáky. Na cvičení se píše jediný soubor
`checks.json`; hodnocení běží v runneru classroom50 a výsledek se objeví jako
komentář ve Feedback PR žáka (body po blocích i celkem, očíslované požadavky,
nápověda, historie odevzdání).

## Jak to funguje

1. Žák pushne. Shim `oa.yaml` v jeho repu zavolá runner classroom50.
2. Runner stáhne balík `TRIDA/autograders/SLUG/` (tento `autograder.py` +
   `checks.json`) a spustí ho. Knihovna zapíše `result.json`
   (`classroom50/result/v1`) a `release-body.md` (česky).
3. Runner publikuje Release a stav commitu.
4. Job `feedback` ze shimu vloží/přepíše komentář ve Feedback PR
   (composite akce `feedback-comment`).

## `checks.json`

```json
{
  "schema": "oa-autograding/checks/v1",
  "title": "Cvičení 10: Markdown",
  "docs": "https://oa-scm-syllabus.github.io/scm_prednasky/10_markdown/",
  "tasks": [
    {
      "id": "ukol-a", "name": "Úkol A", "prefix": "A", "file": "project_readme.md",
      "checks": [
        {"id": "headings", "description": "Nadpisy: H1 a další úroveň", "type": "md.headings",
         "levels_any_of": [2, 3], "points": 1, "hint": "Nadpis první úrovně je `# Název`."}
      ]
    }
  ]
}
```

- `tasks` = bloky s vlastním součtem bodů; `prefix` dává číslování `A1, A2…`.
- `points` (výchozí 1) je váha požadavku; `hint` je pevná nápověda, kontrola
  k ní přidá konkrétní důvod; `docs` je kotva/URL připojená k `docs` z hlavičky.
- `file` bloku je výchozí soubor kontrol, kontrola ho může přepsat.

Typy kontrol: `python -m oa_autograding types`. Parametry každého typu jsou
v docstringu modulu `oa_autograding/checks/*.py`.

## Lokální ověření

```bash
pip install git+https://github.com/adamfiser/oa-autograding@v1-rc
oa-check check --spec checks.json --repo cesta/k/repu
```
Exit 0 = vše splněno, 1 = něco nesplněno, 2 = neplatný `checks.json`.

## Nasazení do classroom50

1. Do `ORG/classroom50` přidej `TRIDA/autograders/oa.yaml` (z `templates/shim.yaml`,
   nahraď `{{ORG}}`) a `TRIDA/autograders/SLUG/{autograder.py,checks.json}`
   (`autograder.py` z `templates/`). Commit + push do `main`; workflow
   `Publish Pages` balík zveřejní (počítej s ~10 min zpožděním Pages).
2. Zaregistruj zadání:
   ```bash
   gh teacher assignment add ORG TRIDA SLUG --name "Název" --template OWNER/SABLONA --autograder oa
   ```
3. Šablona zadání nemá obsahovat `.github/` — shim vzniká při přijetí.

## Vývoj

```bash
pip install -e ".[dev]"
pytest
```
Verze se pinuje tagem (`v1-rc`, `v1`, …). Změna kontroly u běžícího cvičení
= nový tag, zvýšení `VERSION` ve stubu, regrade.

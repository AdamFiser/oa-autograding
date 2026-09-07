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

Postup ověřený 2026-09-07 na pilotu `oa-pva` / `pva2-1sk-ctvrtek-2026-2027` /
`10-markdown` (šablona `oa-scm-syllabus/scm_10_markdown`).

**Předpoklady:** org s plánem Team/Enterprise (Pages na privátním repu
`classroom50`; na plánu Free padá `Publish Pages` s HTTP 422), token `gh` se
scopes `admin:org, read:org, repo, workflow` (`gh auth refresh -h github.com -s
admin:org,read:org,repo,workflow`; nikdy `gh teacher login` — nahrazuje token),
rozšíření `gh teacher` a `gh student`, šablona označená jako template.

1. **Shim a bundle** — v klonu `ORG/classroom50`:
   ```bash
   sed 's/{{ORG}}/ORG/g' templates/shim.yaml > TRIDA/autograders/oa.yaml
   mkdir -p TRIDA/autograders/SLUG
   cp templates/autograder.py TRIDA/autograders/SLUG/
   cp cesta/k/checks.json    TRIDA/autograders/SLUG/
   python -m oa_autograding check --spec TRIDA/autograders/SLUG/checks.json --repo vzorove-reseni
   git add TRIDA/autograders && git commit -m "feat(TRIDA): shim oa a autograder pro SLUG" && git push
   ```
   Ne přes PowerShell 5.1 (`Get-Content`/`Set-Content` rozbijí UTF-8 a přidají BOM).
   Workflow `Publish Pages` doběhne do ~30 s; ověř
   `curl -sI https://ORG.github.io/classroom50/TRIDA/autograders/oa.yaml` a
   `…/autograders/SLUG.tar.gz` → 200 (v pilotu do 1 min od pushe).
2. **Registrace** (zamknuté, dokud není ověřeno):
   ```bash
   gh teacher assignment add ORG TRIDA SLUG --name "Název" --description "…" \
     --template OWNER/SABLONA --autograder oa --locked
   gh teacher autograder list ORG TRIDA        # očekávej oa.yaml + SLUG/
   ```
   `--autograder oa` vyžaduje, aby `TRIDA/autograders/oa.yaml` už bylo v repu.
3. **Šablona** nesmí obsahovat `.github/` — shim vzniká při přijetí a `.github/`
   šablony se přepisuje při každém `gh student submit`. Změnu šablony mergni
   **před** zkouškou přijetí (accept kopíruje `main` šablony).
4. **Zkouška naostro** pod vlastním účtem (musí být v rosteru třídy):
   ```bash
   gh teacher assignment lock ORG TRIDA SLUG --unlock   # odemknutí = klíč locked zmizí
   gh student accept ORG TRIDA SLUG                     # repo ORG/TRIDA-SLUG-login + Feedback PR
   gh teacher assignment lock ORG TRIDA SLUG
   ```
   Pushni kostru (má selhat) a vzorové řešení (má projít); po každém pushi do
   ~1 min: workflow `Autograde` (joby `grade/*` a `feedback`), Release
   `submit/<čas>-<sha7>`, stavy `classroom50/autograde` a
   `classroom50/feedback-pr`, jeden přepisovaný komentář ve Feedback PR:
   ```bash
   gh api repos/ORG/REPO/issues/1/comments --jq '.[] | select(.body | contains("oa-autograding")) | .body'
   ```
   Dva pushe rychle za sebou: první běh `cancelled`, komentář patří poslednímu commitu.
5. **Další třída se stejným cvičením:** `gh teacher assignment reuse` (stejná org)
   a zkopírovat `TRIDA/autograders/oa.yaml` + `SLUG/` do adresáře druhé třídy.

## Vývoj

```bash
pip install -e ".[dev]"
pytest
```
Verze se pinuje tagem (`v1-rc`, `v1`, …). Změna kontroly u běžícího cvičení
= nový tag, zvýšení `VERSION` ve stubu, regrade.

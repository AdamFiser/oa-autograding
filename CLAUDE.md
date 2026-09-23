# oa-autograding — poznámky pro Claude Code

Knihovna kontrol pro classroom50. Architektura, formát `checks.json` a postup
pro tvořitele zadání jsou v README.md — to je vstupní bod projektu (GitHub
z něj renderuje stránku repozitáře) a zůstává na místě.

## Dokumentace

Veškerá další dokumentace (návody, poznámky, rozhodnutí, delší vysvětlení,
která nepatří do README) se ukládá do `.docs/`, ne do kořene projektu.
Nový dokument → `.docs/<téma>.md`.

## Vývoj

```bash
pip install -e ".[dev]"
pytest
```

Verze knihovny se pinuje tagem v CalVer `RRRR.M.N` (`2026.9.0`, `2026.9.1`, `2026.10.0`, …);
starší `v1-rc` zůstává pro běžící cvičení.

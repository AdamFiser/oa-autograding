# TaskFlow

**TaskFlow** je *jednoduchý* nástroj pro správu úkolů z příkazové řádky. ~~Synchronizace přes FTP~~ byla nahrazena cloudovou synchronizací.

## Obsah

- [Funkce](#funkce)
- [Instalace](#instalace)
- [Konfigurace](#konfigurace)

## Funkce

- Přidávání a mazání úkolů
- Štítky
  - barevné štítky
  - vlastní ikony
- Termíny a připomínky
- Export do CSV

## Instalace

1. Nainstalujte Python 3.12 nebo novější.
2. Spusťte instalaci balíčku.
3. Ověřte verzi příkazem `taskflow --version`.

```bash
pip install taskflow
```

## Použití

Nový úkol přidáte parametrem `add`, seznam zobrazí `list`.

## Konfigurace

| Parametr | Výchozí | Popis |
|----------|---------|-------|
| `editor` | `nano` | Editor pro úpravy poznámek |
| `color` | `true` | Barevný výstup |
| `sync` | `false` | Cloudová synchronizace |

## Ukázky a odkazy

![Verze](https://img.shields.io/badge/version-1.0-blue)

![Logo][logo]

Dokumentace je na [webu projektu](https://example.com/taskflow) a ve [wiki][wiki].

[logo]: https://example.com/logo.png
[wiki]: https://example.com/wiki

## Ohlasy uživatelů

> TaskFlow mi ušetří hodinu denně.

## Řešení častých problémů

<details>
<summary>Příkaz taskflow není nalezen</summary>

Zkontrolujte, že je adresář se skripty Pythonu v proměnné PATH.

</details>

## Roadmapa

- [x] Základní správa úkolů
- [x] Štítky
- [ ] Mobilní aplikace

---

Verze 1.0 je vydána pod licencí MIT[^1].

[^1]: Plné znění licence je v souboru LICENSE.

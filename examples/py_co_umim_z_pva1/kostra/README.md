# PVA2 - Programování a vývoj aplikací
## Co umím z PVA1

Vítejte zpět! Než se pustíme do nové látky, potřebuji vědět, kde každý z vás právě je.
Tohle opakování **není na známky** – je to mapa, podle které si naplánujeme, na co navážeme
a co si společně připomeneme.

Ukažte, co umíte:
- Použijte všechno, co jste se v programování naučili – proměnné, podmínky, cykly, funkce,
  seznamy, slovníky, práci s řetězci… Čím víc toho do řešení vložíte, tím lépe.
- Nevíte si s něčím rady? Nevadí. Nevzdávejte to a udělejte, co zvládnete. I částečné
  řešení nebo jen rozpracovaný nápad má cenu.
- Na nedokončenou část napište komentář, jak byste postupovali. I to mi hodně řekne.
- Nezáleží na tom, kolik stihnete, ale co opravdu umíte vy sami.

Úkoly byste měli zvládnout zhruba za 45 minut. Potřebujete-li více času, řekněte si.

Pravidla:
- Pracujte sami, bez pomoci spolužáků.
- Nepoužívejte internet ani AI asistenty (ChatGPT, Copilot apod.). Vývojové prostředí a jeho nápověda povoleny jsou.
- Svůj kód pište do souboru `reseni.py` pod připravená data.

Hodně štěstí – věřím, že toho umíte víc, než si myslíte!

## Hodnocení zakázky

Obchodníci v naší softwarové firmě odhadují šanci na získání zakázky jednoduchým bodovým systémem.
Každá zakázka získá 0 až 10 bodů podle těchto kritérií:

| Kritérium | Klíč v datech | Body |
|---|---|---|
| Odvětví | `odvetvi` | `automotive` 3, `retail` 2, jiné 0 |
| Obrat (mil. EUR) | `obrat` | méně než 10 → 0, od 10 do 1 000 včetně → 3, více než 1 000 → 1 |
| Země | `zeme` | `CZ`, `SK` 2, `DE`, `FR` 1, jiné 0 |
| Účast na loňské konferenci | `konference` | ano 1, ne 0 |
| Odběr newsletteru | `newsletter` | ano 1, ne 0 |

Podle součtu bodů určete šanci na získání zakázky:

| Body | Šance |
|---|---|
| 0–4 | `malá` |
| 5–8 | `střední` |
| 9–10 | `vysoká` |

## Úkoly

### 1. Kontrola vstupních dat
Seznam poptávek `poptavka` v souboru `reseni.py` přepisoval juniorní developer a udělal v něm 5 chyb.
Najděte je a opravte. Ke každé opravě připište komentář `# OPRAVA: ...`.

### 2. Výpočet bodů
Napište funkci, která pro jednu zakázku spočítá body podle zadaných kritérií.
Účast na konferenci a odběr newsletteru ať jsou nepovinné údaje – pokud je nezadáme, počítá se s „ne“.

### 3. Určení šance
Napište funkci, která podle počtu bodů vrátí šanci na získání zakázky jako text.

### 4. Výstupy
Pomocí svých funkcí zpracujte všechny firmy ze seznamu `poptavka` a na obrazovku vypište:
1. šanci a počet bodů každé firmy (ve stejném pořadí jako v seznamu),
2. průměrný počet bodů zaokrouhlený na 2 desetinná místa,
3. názvy **všech** firem s nejvyšším počtem bodů (může jich být více),
4. tři firmy s nejvyšším počtem bodů seřazené sestupně; při shodě bodů zachovejte pořadí ze seznamu.

### Bonus
Zbývá-li vám čas, vypište, kolik firem spadá do každé kategorie šance (`malá`, `střední`, `vysoká`).

### Formát výstupu
Místo `<…>` doplňte skutečné hodnoty.
```
<název> má šanci na získání zakázky: <šance> (body: <body>)
...

Průměrný počet bodů: <průměr>

Firmy s nejvyšším počtem bodů: <název>, <název>, ...

Tři nejlepší firmy:
<název> má šanci na získání zakázky: <šance> (body: <body>)
...

Počet firem podle šance:
malá: <počet>
střední: <počet>
vysoká: <počet>
```

### Očekávaný výstup
Podle něj si můžete ověřit, zda váš program počítá správně.
```
Firma A má šanci na získání zakázky: vysoká (body: 10)
Firma B má šanci na získání zakázky: střední (body: 8)
Firma C má šanci na získání zakázky: střední (body: 5)
Firma D má šanci na získání zakázky: malá (body: 4)
Firma E má šanci na získání zakázky: vysoká (body: 9)
Firma F má šanci na získání zakázky: střední (body: 8)
Firma G má šanci na získání zakázky: střední (body: 6)
Firma H má šanci na získání zakázky: střední (body: 6)
Firma I má šanci na získání zakázky: vysoká (body: 10)
Firma J má šanci na získání zakázky: střední (body: 8)
Firma K má šanci na získání zakázky: střední (body: 7)
Firma L má šanci na získání zakázky: střední (body: 6)
Firma M má šanci na získání zakázky: malá (body: 3)
Firma N má šanci na získání zakázky: malá (body: 4)
Firma O má šanci na získání zakázky: střední (body: 7)

Průměrný počet bodů: 6.73

Firmy s nejvyšším počtem bodů: Firma A, Firma I

Tři nejlepší firmy:
Firma A má šanci na získání zakázky: vysoká (body: 10)
Firma I má šanci na získání zakázky: vysoká (body: 10)
Firma E má šanci na získání zakázky: vysoká (body: 9)

Počet firem podle šance:
malá: 3
střední: 9
vysoká: 3
```

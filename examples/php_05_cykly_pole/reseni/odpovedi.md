# Odpovědi — PHP 05: Cykly a pole (klíč pro učitele)

## ÚKOL 1 — nová stránka v menu

Jeden soubor (`includes/config.php`) a jeden řádek v poli `menu`.
V PHP_06 se kopíroval celý odkaz `<a>` s podmínkou v `templates/menu.php`.

## ÚKOL 7 — `while` a `do...while` při `$pagesTotal = 0`

`while` vypíše `za 0 týdnů` — podmínka `0 < 0` neplatí už před prvním
průchodem. `do...while` vypíše `za 1 týdnů` — tělo se provede alespoň
jednou, podmínka se testuje až po průchodu.

## ÚKOL 8 — Co vypíše?

**Vypíše:** `6`

**Proč:** sečte se 2 a 1, pětku `continue` přeskočí, přičte se 3,
čtyřka `break` cyklus ukončí — poslední jednička se už nesečte.

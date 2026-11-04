# Odpovědi — PHP 07: Funkce (klíč pro učitele)

## ÚKOL 3 — co bylo špatně na `printDeadline()`

1. Výsledek **vypisovala** (`echo`) místo `return` — text ani třídu nešlo
   použít jinde, než kde byla funkce zavolána (např. v e-mailu, v podmínce).
2. Data si brala přes **`global`** — z hlavičky nebylo vidět, co potřebuje,
   a fungovala jen tehdy, když na stránce náhodou existovaly proměnné
   `$daysLeft`, `$daysCount` a `$daysWord`.

(Uznat i: dělala dvě věci naráz — text i barvu; chyběly typy.)

## ÚKOL 9 — strict types a hodnota z adresy

Stránka skončí chybou `TypeError`: `getGreeting(): Argument #1 ($hour) must be
of type int, string given`. Hodnoty z adresy (`$_GET`) jsou vždy řetězce
(`'7'`) a se `declare(strict_types=1);` PHP řetězec na `int` potichu
nepřevede. Proto hodnotu před předáním funkci převedeme `(int)`.

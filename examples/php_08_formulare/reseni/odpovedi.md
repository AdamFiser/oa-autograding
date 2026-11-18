# Odpovědi — PHP 08: Formuláře

## ÚKOL 5 — proč přesměrovat po odeslání

Prohlížeč se zeptal, jestli má formulář odeslat znovu, a po potvrzení poslal stejný POST ještě jednou — dotaz by se přijal dvakrát. Po přesměrování je poslední požadavek GET na `contact.php?odeslano=1`, takže F5 jen znovu načte stránku s poděkováním.

## ÚKOL 7 — proč ne původní název souboru

1. Název volí uživatel: `foto.php` by se uložil jako spustitelný skript a útočník by ho spustil přes `uploads/foto.php`.
2. Dva soubory se stejným názvem by se přepsaly a název může obsahovat nebezpečné znaky (`../`, mezery, diakritiku).

## ÚKOL 9 — podvržená hodnota

Formulář ukázal chybu `Vyberte typ dotazu.` — hodnotu `hack` odmítla funkce `nactiVolbu()`, protože není v seznamu povolených typů, a vrátila `null`.

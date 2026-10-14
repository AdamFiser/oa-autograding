# Odpovědi — PHP 04: Podmínky (klíč pro učitele)

## ÚKOL 6a — `==` a `===`

**Vypíše:** `AC`

**Proč:** `'0' == false` převede řetězec `'0'` na `false`, takže platí. `===`
porovnává i typ — řetězec není `bool`, `B` se nevypíše. `'0' === '0'` platí.

## ÚKOL 6b — `and` a `&&`

**Vypíše:** `ano / ne`

**Proč:** `=` má vyšší prioritu než `and`, do `$smiOdevzdat` se uloží jen
`$maTema` (`true`). `&&` se vyhodnotí před přiřazením.

## ÚKOL 6c — zapomenutý `break`

**Vypíše:** `čeká zamítnuto `

**Proč:** bez `break` pokračuje `switch` od nalezeného `case 'pending'`
dalšími větvemi až k nejbližšímu `break`.

`match ($status) { 'approved' => 'schváleno', 'pending' => 'čeká', 'rejected' => 'zamítnuto', default => 'neznámý' }`
— `match` nepropadá do dalších větví a porovnává přes `===`.

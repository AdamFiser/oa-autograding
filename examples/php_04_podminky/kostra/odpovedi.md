# Odpovědi — PHP 04: Podmínky

Ke každému úryvku napište, co vypíše, a jednou větou proč.

## ÚKOL 6a — `==` a `===`

```php
$pocet = '0';

if ($pocet == false) {
    echo 'A';
}
if ($pocet === false) {
    echo 'B';
}
if ($pocet === '0') {
    echo 'C';
}
```

**Vypíše:**

**Proč:**

## ÚKOL 6b — `and` a `&&`

```php
$maTema = true;
$maKonzultace = false;

$smiOdevzdat = $maTema and $maKonzultace;
$smiOdevzdat2 = $maTema && $maKonzultace;

echo $smiOdevzdat ? 'ano' : 'ne';
echo ' / ';
echo $smiOdevzdat2 ? 'ano' : 'ne';
```

**Vypíše:**

**Proč:**

## ÚKOL 6c — zapomenutý `break`

```php
$status = 'pending';

switch ($status) {
    case 'approved':
        echo 'schváleno ';
    case 'pending':
        echo 'čeká ';
    case 'rejected':
        echo 'zamítnuto ';
        break;
    default:
        echo 'neznámý';
}
```

**Vypíše:**

**Proč:**

Jak byste stejný převod napsali přes `match`, aby se chyba nemohla stát?

# Odpovědi — PHP 05: Cykly a pole

## ÚKOL 1 — nová stránka v menu

Kolik souborů a řádků teď upravíte? Kolik to bylo v PHP_06?


## ÚKOL 7 — `while` a `do...while` při `$pagesTotal = 0`


## ÚKOL 8 — Co vypíše?

```php
$znamky = [2, 1, 5, 3, 4, 1];
$soucet = 0;

foreach ($znamky as $znamka) {
    if ($znamka === 5) {
        continue;
    }
    if ($znamka === 4) {
        break;
    }
    $soucet += $znamka;
}

echo $soucet;
```

**Vypíše:**

**Proč:**

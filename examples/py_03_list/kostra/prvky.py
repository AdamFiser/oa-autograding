# Úkol C – Přiřazení do řezu a opakování seznamu
#
# Přiřazení je možné k řezům seznamů, stejně jako k jednotlivým prvkům seznamu.
# Tímto způsobem lze dokonce měnit velikost seznamu nebo jej zcela vymazat pomocí příkazu animals[:] = []
#
# Místo `...` doplňte své řešení.

animals = ["elephant", "lion", "tiger", "giraffe", "monkey", "dog"]  # Vytvoření nového seznamu
print(animals)

animals[1:3] = ["cat"]    # Nahrazení 2 položek -- "lion" a "tiger" jednou položkou -- "cat".
print(animals)

animals[1:3] = []     # Odstranění 2 položek -- "cat" a "giraffe" ze seznamu
print(animals)

# C1 Přiřazením do řezu nahraďte poslední dvě položky tak, aby ze všech zvířat byli sloni.
#    Očekávaný výstup: ['elephant', 'elephant', 'elephant']

print(animals)

# C2 Pomocí opakování seznamu operátorem * uložte do `nuly` seznam s deseti nulami.
nuly = ...
print(nuly)

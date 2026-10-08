# Úkol A – Indexy a řezy
#
# Python má řadu složených datových typů, které se používají ke sdružování dat.
# Nejuniverzálnější je list (seznam), který lze zapsat jako řadu čárkou oddělených hodnot (položek) uzavřených v hranatých závorkách,
# např. lst = [polozka1, polozka2].
# Seznamy mohou obsahovat položky různých typů, ale obvykle jsou všechny položky v seznamu stejného typu.
# Stejně jako řetězce lze seznamy indexovat a používat řezy (viz předchozí cvičení).
# Všechny operace slice vracejí nový seznam obsahující požadované prvky.
#
# Místo `...` doplňte své řešení.

squares = [1, 4, 9, 16, 25]   # Vytvoření nového seznamu
print(squares)

# A1 Pomocí řezu uložte do `stred` prvky [4, 9, 16]
stred = squares[1:4]
print(stred)

# A2 Pomocí záporného indexu uložte do `predposledni` předposlední prvek seznamu
predposledni = squares[-2]
print(predposledni)

# A3 Pomocí řezu s krokem uložte do `kazdyDruhy` prvky [1, 9, 25]
kazdyDruhy = squares[::2]
print(kazdyDruhy)

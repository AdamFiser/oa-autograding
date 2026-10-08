# Úkol B – Přidání, vložení a odstranění prvků
#
# Místo `...` doplňte své řešení. Úkoly B1 až B4 měňte přímo seznam `animals`.

animals = ["elephant", "lion", "tiger", "giraffe"]  # Vytvoření nového seznamu
print(animals)

animals += ["monkey", "dog"]    # Přidání dvou položek do seznamu
print(animals)

animals.append("dino")   # Přidání další položky do seznamu pomocí metody append()
print(animals)

# B1 Nahraďte původní "dino" za "dinosaurus".
#    Pro nalezení indexu prvku v seznamu můžete použít metodu index().
animals[animals.index("dino")] = "dinosaurus"

print(animals)

# B2 Na začátek seznamu vložte "zebra" metodou insert().
animals.insert(0, "zebra")

print(animals)

# B3 Ze seznamu odstraňte "lion" metodou remove().
animals.remove("lion")

print(animals)

# B4 Metodou pop() odeberte prvek na indexu 1 a uložte ho do `odebrany`.
odebrany = animals.pop(1)
print(odebrany)
print(animals)

# B5 Do `maTygra` uložte výsledek testu operátorem in, zda je "tiger" v seznamu (True / False).
maTygra = "tiger" in animals
print(maTygra)

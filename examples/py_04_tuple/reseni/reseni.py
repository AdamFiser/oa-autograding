alphabet = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
            'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')

# Reseni 1
delka = len(alphabet)
print(delka)


# Reseni 2
onlyOne = ('Python',)
print(onlyOne, type(onlyOne))


# Reseni 3
profese = ('Strojvedoucí', 'Vlakvedoucí', 'Vozmistr')
print(profese)


# Reseni 4
souradnice = (11, 22)
souradnice = souradnice + (33,)
souradnice = souradnice[1:]

print(souradnice)

# Vysvětlení: ntice je neměnná (immutable), nemá append() ani del prvku, proto vzniká nová.


# Reseni 5
prvni = alphabet[0]
druhy = alphabet[1]


# Reseni 6
posledni = alphabet[-1]
predposledni = alphabet[-2]


# Reseni 7
kazdyTreti = alphabet[::3]


# Reseni 8
prvnichPet = alphabet[:5]


# Reseni 9
poslednichPet = alphabet[-5:]


# Reseni 10
prvniPulka = alphabet[:len(alphabet) // 2]


# Reseni 11
datum = (2026, 10, 1)
rok, mesic, den = datum


# Reseni 12
designPatterns = ('Adapter', 'Repository', 'Facade', 'Factory')
indexRepository = designPatterns.index('Repository')
indexFactory = designPatterns.index('Factory')

# Co se stane pro 'repository': ValueError, index() rozlišuje velká a malá písmena.


# Reseni 13
x = input("x: ")
y = input("y: ")
z = input("z: ")
hodnoty = (x, y, z)
print(hodnoty)
print(f"Počet výskytů – x: {hodnoty.count(x)}, y: {hodnoty.count(y)}, z: {hodnoty.count(z)}")


# Reseni 14
print(f"Byly zadány hodnoty x: {x}, y: {y}, z: {z} a jejich součet je: {int(x) + int(y) + int(z)}")


# Úkol 1
prirozena = []
for i in range(1, 11):
    prirozena.append(i)
print(prirozena)


# Úkol 2
licha = []
for i in range(1, 20, 2):
    licha.append(i)
print(licha)


# Úkol 3
odpocet = []
for i in range(10, 0, -1):
    odpocet.append(i)
print(odpocet)


# Úkol 4
n = 100
soucet = 0
for i in range(1, n + 1):
    soucet += i
print(soucet)


# Úkol 5
text = "Hello, World!"
delka = 0
for znak in text:
    delka += 1
print(delka)


# Úkol 6
ovoce = ["jablko", "banán", "třešeň"]
ocislovane = []
for poradi, kus in enumerate(ovoce, start=1):
    ocislovane.append(f"{poradi}. {kus}")
print(ocislovane)


# Úkol 7
sklad = {"jablka": 12, "hrušky": 0, "švestky": 5, "meruňky": 0}
vyprodano = []
for zbozi, kusu in sklad.items():
    if kusu == 0:
        vyprodano.append(zbozi)
print(vyprodano)


# Úkol 8
body = {"Adam": 85, "Bára": 67, "Cyril": 73, "Dana": 92, "Eva": 58}
celkem_bodu = 0
for pocet in body.values():
    celkem_bodu += pocet
print(celkem_bodu)


# Úkol 9
nejlepsi = None
for jmeno, pocet in body.items():
    if nejlepsi is None or pocet > body[nejlepsi]:
        nejlepsi = jmeno
print(nejlepsi)


# Úkol 10
prospeli = []
for jmeno, pocet in body.items():
    if pocet >= 60:
        prospeli.append(jmeno)
print(prospeli)


# Úkol 11
cenik = {"chléb": 40, "mléko": 25, "máslo": 60}
cenik_dph = {}
for zbozi, cena in cenik.items():
    cenik_dph[zbozi] = round(cena * 1.21, 2)
print(cenik_dph)


# Úkol 12
veta = "jablko hruška jablko švestka hruška jablko"
cetnost = {}
for slovo in veta.split():
    cetnost[slovo] = cetnost.get(slovo, 0) + 1
print(cetnost)


# Úkol 13
znamky = {"Adam": [1, 2, 3], "Bára": [1, 1, 1], "Cyril": [2, 3, 4]}
prumery = {}
for jmeno, seznam in znamky.items():
    soucet_znamek = 0
    for znamka in seznam:
        soucet_znamek += znamka
    prumery[jmeno] = soucet_znamek / len(seznam)
print(prumery)


# Úkol 14
vzor = []
for radek in range(1, 6):
    cisla = ""
    for cislo in range(1, radek + 1):
        cisla += str(cislo) + " "
    vzor.append(cisla.strip())
print(vzor)


# Úkol 15
teploty = [3, 5, -2, 4, -7]
prvni_zaporna = None
for teplota in teploty:
    if teplota < 0:
        prvni_zaporna = teplota
        break
print(prvni_zaporna)


# Úkol 16
mereni = [12, -1, 15, 9, -1, 14]
platna = []
for hodnota in mereni:
    if hodnota == -1:
        continue
    platna.append(hodnota)
print(platna)


# Úkol 17
zaci = ["Adam", "Petr", "Jana"]
hledane = "Eva"
for zak in zaci:
    if zak == hledane:
        zprava = f"{hledane} je ve třídě"
        break
else:
    zprava = f"{hledane} ve třídě není"
print(zprava)


# Úkol 18
mocniny = []
cislo = 1
while cislo ** 2 <= 81:
    mocniny.append(cislo ** 2)
    cislo += 1
print(mocniny)


# Úkol 19
cil = 1000
tydne = 150
tydny = 0
usetreno = 0
while usetreno < cil:
    usetreno += tydne
    tydny += 1
print(tydny)

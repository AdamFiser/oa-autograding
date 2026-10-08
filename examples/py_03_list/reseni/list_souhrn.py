# Úkol E – List souhrn
#
# Místo `...` doplňte své řešení. Výsledky ukládejte do uvedených proměnných
# a vypisujte je, ať vidíte, co program spočítal.


# E1
#
# Seznam `mocniny` obsahuje mocniny čísla 2.
# 1. Na konec seznamu přidejte 2 na 6 a 2 na 7 (vypočítejte operátorem **).
# 2. Odeberte první prvek.

mocniny = [1, 2, 4, 8, 16, 32]
mocniny.append(2 ** 6)
mocniny.append(2 ** 7)
del mocniny[0]

print(mocniny)


# E2
#
# Prohoďte první prvek seznamu `cisla` s třetím. Výsledek uložte do `result`,
# původní seznam `cisla` se nesmí změnit. Oba seznamy vytiskněte.
#
# Očekávaný výstup: [23, 65, 19, 90] a [19, 65, 23, 90]

cisla = [23, 65, 19, 90]
result = [cisla[2], cisla[1], cisla[0], cisla[3]]
print(cisla)
print(result)


# E3
#
# Ze seznamu `barvy` odstraňte první, čtvrtý a pátý prvek a seznam vytiskněte.
# Pozor: po odstranění prvku se indexy dalších prvků posunou.
#
# Očekávaný výstup: ['Green', 'White', 'Yellow']

barvy = ['Red', 'Green', 'White', 'Black', 'Pink', 'Yellow']
del barvy[4]
del barvy[3]
del barvy[0]

print(barvy)


operation = [1456, 5, 98, 4087, 12, 448, 4, 8, 14, 264, 10, 88, 379, 32, 2971]

# E4
#
# Pomocí funkcí pro hledání extrémních hodnot uložte nejmenší prvek seznamu `operation`
# do `nejmensi` a největší do `nejvetsi`. Výsledek s popiskem vytiskněte.

nejmensi = min(operation)
nejvetsi = max(operation)
print('Nejmenší:', nejmensi, 'největší:', nejvetsi)


# E5
#
# Nejmenší a největší prvek najděte jiným způsobem než funkcemi min() a max()
# (např. pomocí seřazeného seznamu). Uložte je do `nejmensi2` a `nejvetsi2`.

nejmensi2 = sorted(operation)[0]
nejvetsi2 = sorted(operation)[-1]


# E6
#
# Do `obracene` uložte prvky seznamu `operation` v opačném pořadí,
# tzn. první prvek bude poslední, druhý předposlední atd.

obracene = operation[::-1]
print(obracene)


cars = ['Suzuki', 'Lamborghini', 'lexus', 'porsche', 'Ferrari', 'vojvo', 'chevrolet', 'DS', 'Jeep', 'Mini', 'Škoda']

# E7
#
# V seznamu `cars` nahraďte značku auta 'vojvo' hodnotou 'Volvo'.
cars[cars.index('vojvo')] = 'Volvo'

print(cars)


# E8
#
# Ze seznamu `cars` zkopírujte druhý až čtvrtý prvek do nového seznamu `luxuryCars`.

luxuryCars = cars[1:4]
print(luxuryCars)


# E9
#
# Součet všech prvků seznamu `operation` uložte do proměnné `operationSum`.

operationSum = sum(operation)
print(operationSum)


# E10
#
# Počet aut v seznamu `cars` uložte do `pocetAut`.

pocetAut = len(cars)
print(pocetAut)


# E11
#
# Index auta 'Ferrari' v seznamu `cars` uložte do `indexFerrari`.

indexFerrari = cars.index('Ferrari')
print(indexFerrari)


# E12
#
# Do `serazenaAuta` uložte seřazený seznam aut. Původní seznam `cars` se nesmí změnit.
# Všimněte si, kam se seřadily značky psané malým písmenem.

serazenaAuta = sorted(cars)
print(serazenaAuta)
print(cars)


# E13
#
# Zamyslete se, co provede následující kód. Nejdřív si tipněte, pak kód spusťte.
#
# myList1 = [1, 2, 3, 4]
# myList2 = myList1
# myList1.append(5)
#
# 1. Do `odpoved` uložte (jako seznam) obsah `myList2` po provedení kódu.
# 2. Formou komentáře vysvětlete, proč tomu tak je.

odpoved = [1, 2, 3, 4, 5]

# Vysvětlení: myList2 = myList1 nevytvoří kopii, obě proměnné ukazují na stejný seznam.

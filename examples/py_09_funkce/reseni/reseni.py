# Cvičení 09: Funkce – vzorové řešení


# Úkol 1
def pozdrav() -> None:
    print("Hello world")


pozdrav()


# Úkol 2
def pozdravKrat(pocet: int) -> None:
    for i in range(pocet):
        pozdrav()


pozdravKrat(3)


# Úkol 3
def druhaMocnina(cislo: int) -> int:
    return cislo * cislo


for cislo in [4, 8, 15, 23, -1]:
    print(druhaMocnina(cislo))


# Úkol 4
def soucetDvou(a: float, b: float) -> float:
    return a + b


print(soucetDvou(2, 4) + soucetDvou(10, 5))


# Úkol 5
def vypocet(a: int, b: int = 2, c: int = 10) -> int:
    return a * b + c


print(vypocet(3, 5, 20), vypocet(3, 5), vypocet(3))


# Úkol 6
def jeSude(cislo: int) -> bool:
    return cislo % 2 == 0


print(jeSude(4), jeSude(7))


# Úkol 7
def minMax(cisla: list[int]) -> tuple[int, int]:
    nejmensi = cisla[0]
    nejvetsi = cisla[0]
    for cislo in cisla:
        if cislo < nejmensi:
            nejmensi = cislo
        if cislo > nejvetsi:
            nejvetsi = cislo
    return nejmensi, nejvetsi


nejmensi, nejvetsi = minMax([3, 1, 2])
print(nejmensi, nejvetsi)


# Úkol 8
barvy = ["red", "green", "blue", "white"]


def pridejUnikatni(seznam: list[str], prvek: str) -> None:
    if prvek not in seznam:
        seznam.append(prvek)


pridejUnikatni(barvy, "red")
pridejUnikatni(barvy, "black")
print(barvy)


# Úkol 9
barvySOpakovanim = ["red", "green", "blue", "white", "red", "black", "orange", "black"]


def bezDuplicit(seznam: list[str]) -> list[str]:
    vysledek = []
    for prvek in seznam:
        if prvek not in vysledek:
            vysledek.append(prvek)
    return vysledek


print(bezDuplicit(barvySOpakovanim))


# Úkol 10
cisla1 = [-14, -12, -10, 1, 2, 3]
cisla2 = [1, 1, 1, -11, -11, -11]


def soucetVybranych(cisla: list[int]) -> int:
    soucet = 0
    for cislo in cisla:
        if cislo > 0 or cislo < -10:
            soucet += cislo
    return soucet


print("Součet čísel, která jsou kladná, nebo jsou menší než -10 je", soucetVybranych(cisla1))
print("Součet čísel, která jsou kladná, nebo jsou menší než -10 je", soucetVybranych(cisla2))


# Úkol 11
def faktorial(n: int) -> int:
    """Vrátí faktoriál čísla n, faktoriál 0 je 1."""
    if n <= 1:
        return 1
    return n * faktorial(n - 1)


print(faktorial(5))


# Úkol 12
def hodnotaSlova(slovo: str) -> int:
    body = 0
    for znak in slovo.lower():
        if znak == "x":
            body += 10
        elif znak in "aeiouyáéěíóúůý":
            body += 3
        elif znak.isalpha():
            body += 1
    return body


print(hodnotaSlova("python"))

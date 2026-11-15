# Úkol B – SMS brána – vzorové řešení


def jePlatneCislo(cislo: str) -> bool:
    cislo = cislo.replace(" ", "")
    if cislo.startswith("+420"):
        cislo = cislo[4:]
    return len(cislo) == 9 and cislo.isdigit()


def cenaZpravy(text: str) -> int:
    return (len(text) + 179) // 180 * 3


cislo = input("Telefonní číslo: ")
if jePlatneCislo(cislo):
    zprava = input("Text zprávy: ")
    print(f"Zpráva bude stát {cenaZpravy(zprava)} Kč.")
else:
    print("Neplatné telefonní číslo.")

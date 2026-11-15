# Úkol E – Rodné číslo – vzorové řešení


def jeZena(rc: str) -> bool:
    return int(rc[2:4]) > 50


def pocetDni(rok: int, mesic: int) -> int:
    if mesic == 2:
        prestupny = rok % 4 == 0 and (rok % 100 != 0 or rok % 400 == 0)
        return 29 if prestupny else 28
    if mesic in (4, 6, 9, 11):
        return 30
    return 31


def datumNarozeni(rc: str) -> tuple[int, int, int]:
    cislo = rc.replace("/", "")
    rok = int(cislo[0:2])
    mesic = int(cislo[2:4])
    den = int(cislo[4:6])
    if mesic > 50:
        mesic -= 50
    if mesic > 20:
        mesic -= 20
    if len(cislo) == 9 or rok >= 54:
        rok += 1900
    else:
        rok += 2000
    return rok, mesic, den


def jePlatneRodneCislo(rc: str) -> bool:
    cislo = rc.replace("/", "")
    if not cislo.isdigit() or len(cislo) not in (9, 10):
        return False
    rok, mesic, den = datumNarozeni(cislo)
    if len(cislo) == 9 and rok >= 1954:
        return False
    if len(cislo) == 10:
        zbytek = int(cislo[:9]) % 11
        if not (int(cislo) % 11 == 0 or (zbytek == 10 and cislo[9] == "0")):
            return False
    return 1 <= mesic <= 12 and 1 <= den <= pocetDni(rok, mesic)


def vek(rc: str, rok: int, mesic: int, den: int) -> int:
    rokNarozeni, mesicNarozeni, denNarozeni = datumNarozeni(rc)
    roky = rok - rokNarozeni
    if (mesic, den) < (mesicNarozeni, denNarozeni):
        roky -= 1
    return roky


rc = input("Rodné číslo: ")
if jePlatneRodneCislo(rc):
    rok, mesic, den = datumNarozeni(rc)
    pohlavi = "žena" if jeZena(rc) else "muž"
    print(f"Narozen(a) {den}. {mesic}. {rok}, {pohlavi}, věk {vek(rc, 2026, 11, 15)} let")
else:
    print("Neplatné rodné číslo")

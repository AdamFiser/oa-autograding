# Úkol D – Košík – vzorové řešení

cenik = {"tričko": 250, "mikina": 690, "čepice": 180, "ponožky": 90}


def pridejDoKosiku(zbozi: str, kosik: list[str] | None = None) -> list[str]:
    if kosik is None:
        kosik = []
    kosik.append(zbozi)
    return kosik


def odeberZKosiku(kosik: list[str], zbozi: str) -> bool:
    if zbozi in kosik:
        kosik.remove(zbozi)
        return True
    return False


def souhrnKosiku(kosik: list[str]) -> dict[str, int]:
    souhrn = {}
    for zbozi in kosik:
        souhrn[zbozi] = souhrn.get(zbozi, 0) + 1
    return souhrn


def cenaKosiku(kosik: list[str], cenik: dict[str, float]) -> float:
    cena = 0
    for zbozi in kosik:
        if zbozi in cenik:
            cena += cenik[zbozi]
    return cena


def cenaObjednavky(cenaZbozi: float, slevaProcent: float = 0, doprava: float = 99) -> float:
    cena = cenaZbozi - cenaZbozi * slevaProcent / 100
    if cena < 1500:
        cena += doprava
    return round(cena, 2)


kosik = pridejDoKosiku("tričko")
pridejDoKosiku("mikina", kosik)
pridejDoKosiku("tričko", kosik)
odeberZKosiku(kosik, "mikina")
print(souhrnKosiku(kosik))
cena = cenaKosiku(kosik, cenik)
print(cenaObjednavky(cena, slevaProcent=10))
print(cenaObjednavky(cena, doprava=0))

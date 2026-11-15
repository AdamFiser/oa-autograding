# Úkol A – Hodnocení zakázky – vzorové řešení


def bodyZakazky(odvetvi: str, obrat: float, zeme: str, konference: bool = False, newsletter: bool = False) -> int:
    """Vrátí počet bodů zakázky (0 až 10)."""
    body = 0
    if odvetvi == "automotive":
        body += 3
    elif odvetvi == "retail":
        body += 2

    if 10 <= obrat <= 1000:
        body += 3
    elif obrat > 1000:
        body += 1

    if zeme in ("CZ", "SK"):
        body += 2
    elif zeme in ("DE", "FR"):
        body += 1

    if konference:
        body += 1
    if newsletter:
        body += 1
    return body


def sanceZakazky(body: int) -> str:
    """Převede body zakázky na šanci na její získání."""
    if body <= 5:
        return "malá"
    if body <= 8:
        return "střední"
    return "vysoká"


def hodnoceniZakazky(odvetvi: str, obrat: float, zeme: str, konference: bool = False, newsletter: bool = False) -> str:
    """Vrátí šanci na získání zakázky."""
    return sanceZakazky(bodyZakazky(odvetvi, obrat, zeme, konference, newsletter))


print(hodnoceniZakazky("automotive", 500, "CZ", newsletter=True))

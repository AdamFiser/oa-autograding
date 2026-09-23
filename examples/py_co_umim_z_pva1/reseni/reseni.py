
poptavka = [
    {"nazev": "Firma A", "odvetvi": "automotive", "obrat": 50, "zeme": "CZ", "konference": True, "newsletter": True},
    {"nazev": "Firma B", "odvetvi": "retail", "obrat": 500, "zeme": "SK", "konference": False, "newsletter": True},
    {"nazev": "Firma C", "odvetvi": "automotive", "obrat": 5, "zeme": "DE", "konference": True, "newsletter": False},  # OPRAVA: obrat je číslo, ne text
    {"nazev": "Firma D", "odvetvi": "retail", "obrat": 1500, "zeme": "FR", "konference": False, "newsletter": False},
    # OPRAVA: překlep v odvětví Firmy E (autmotive)
    {"nazev": "Firma E", "odvetvi": "automotive", "obrat": 20, "zeme": "CZ", "konference": True, "newsletter": False},  # OPRAVA: obrat je číslo, ne text
    {"nazev": "Firma F", "odvetvi": "retail", "obrat": 800, "zeme": "SK", "konference": False, "newsletter": True},
    {"nazev": "Firma G", "odvetvi": "automotive", "obrat": 2000, "zeme": "DE", "konference": True, "newsletter": False},
    {"nazev": "Firma H", "odvetvi": "retail", "obrat": 50, "zeme": "FR", "konference": False, "newsletter": False},
    {"nazev": "Firma I", "odvetvi": "automotive", "obrat": 100, "zeme": "CZ", "konference": True, "newsletter": True},  # OPRAVA: obrat je číslo, ne text
    {"nazev": "Firma J", "odvetvi": "retail", "obrat": 300, "zeme": "SK", "konference": False, "newsletter": True},
    {"nazev": "Firma K", "odvetvi": "finance", "obrat": 200, "zeme": "CZ", "konference": True, "newsletter": True},
    {"nazev": "Firma L", "odvetvi": "healthcare", "obrat": 700, "zeme": "SK", "konference": False, "newsletter": True},
    {"nazev": "Firma M", "odvetvi": "technology", "obrat": 1200, "zeme": "DE", "konference": True, "newsletter": False},
    {"nazev": "Firma N", "odvetvi": "education", "obrat": 300, "zeme": "FR", "konference": False, "newsletter": False},
    {"nazev": "Firma O", "odvetvi": "energy", "obrat": 900, "zeme": "CZ", "konference": True, "newsletter": True}  # OPRAVA: překlep v klíči newsletter
]

### Níže napište svůj kód ###

BODY_ODVETVI = {"automotive": 3, "retail": 2}
BODY_ZEME = {"CZ": 2, "SK": 2, "DE": 1, "FR": 1}


def spocitej_body(zakazka):
    body = BODY_ODVETVI.get(zakazka["odvetvi"], 0)
    obrat = zakazka["obrat"]
    if obrat > 1000:
        body += 1
    elif obrat >= 10:
        body += 3
    body += BODY_ZEME.get(zakazka["zeme"], 0)
    if zakazka.get("konference", False):
        body += 1
    if zakazka.get("newsletter", False):
        body += 1
    return body


def urci_sanci(body):
    if body >= 9:
        return "vysoká"
    if body >= 5:
        return "střední"
    return "malá"


def vypis(zakazka, body):
    print(f"{zakazka['nazev']} má šanci na získání zakázky: {urci_sanci(body)} (body: {body})")


vysledky = [(zakazka, spocitej_body(zakazka)) for zakazka in poptavka]
for zakazka, body in vysledky:
    vypis(zakazka, body)

prumer = sum(body for _, body in vysledky) / len(vysledky)
print()
print(f"Průměrný počet bodů: {round(prumer, 2)}")

nejvic = max(body for _, body in vysledky)
nejlepsi = [zakazka["nazev"] for zakazka, body in vysledky if body == nejvic]
print()
print(f"Firmy s nejvyšším počtem bodů: {', '.join(nejlepsi)}")

print()
print("Tři nejlepší firmy:")
for zakazka, body in sorted(vysledky, key=lambda v: v[1], reverse=True)[:3]:
    vypis(zakazka, body)

pocty = {"malá": 0, "střední": 0, "vysoká": 0}
for _, body in vysledky:
    pocty[urci_sanci(body)] += 1
print()
print("Počet firem podle šance:")
for sance, pocet in pocty.items():
    print(f"{sance}: {pocet}")

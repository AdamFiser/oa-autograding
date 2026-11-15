# Úkol D – Košík – vzorové řešení


def pridejDoKosiku(zbozi: str, kosik: list[str] | None = None) -> list[str]:
    if kosik is None:
        kosik = []
    kosik.append(zbozi)
    return kosik


print(pridejDoKosiku("tričko"))
print(pridejDoKosiku("mikina"))

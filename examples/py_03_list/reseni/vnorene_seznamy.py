# Úkol D – Vnořené seznamy
#
# Seznam může obsahovat libovolné objekty, dokonce i jiné seznamy (podseznamy).
# Tato datová struktura se nazývá vnořený seznam.
# Vnořené seznamy můžete použít k uspořádání dat do hierarchických struktur.
#
# Vnořený seznam lze vytvořit zápisem posloupnosti podseznamů oddělených čárkou:
#
#   nested_list = [[1, 2, 3], [4, 5], 6]
#
# K položkám vnořeného seznamu můžete přistupovat pomocí indexů stejně jako dříve:
#
#   print(nested_list[1])     # [4, 5]
#   print(nested_list[2])     # 6
#
# K položkám v rámci vnořených seznamů můžete přistupovat pomocí více indexů.
# Pro přístup k číslu 1 použijte dvakrát index 0. Nejprve přistupujete k prvku [1, 2, 3]
# a poté k prvnímu prvku tohoto vnořeného seznamu:
#
#   print(nested_list[0][0])  # 1
#
# Místo `...` doplňte své řešení – použijte indexování, ne přímo číslo.

my_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9], 10]

# D1 Do `devet` uložte pomocí indexování číslo 9 z vnořeného seznamu my_list.
devet = my_list[2][2]
print('Číslo 9 z vnořeného seznamu:', devet)

# D2 Do `deset` uložte pomocí indexování číslo 10 ze seznamu my_list.
deset = my_list[3]
print('Číslo 10 z vnořeného seznamu:', deset)

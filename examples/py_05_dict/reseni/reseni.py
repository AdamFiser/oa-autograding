#Reseni 1
zamestnanec = {'name': 'Jan', 'surname': 'Novák', 'salary': 30000}


#Reseni 2
zamestnanec['salary'] = zamestnanec['salary'] * 1.06


#Reseni 3
employees = {
    'emp1': {'name': 'John', 'surname': 'Doe', 'salary': 32000},
    'emp2': {'name': 'Emma', 'surname': 'Phillips', 'salary': 28000}
}
employees['emp3'] = zamestnanec


#Reseni 4
emp2Hodnoty = list(employees['emp2'].values())
print(emp2Hodnoty)


#Reseni 5
emp_selected = {
    "name": "Maria",
    "age": 34,
    "salary": 47000,
    "city": "Prague"
}
emp_selected["location"] = emp_selected.pop("city")

print(emp_selected)


#Reseni 6
del emp_selected["age"]
del emp_selected["salary"]

print(emp_selected)


#Reseni 7
grades = {
    'Czech': 85,
    'Chemistry': 67,
    'History': 73,
    'Economics': 88,
    'Physics': 64,
    'Computer Science': 91,
    'Mathematics': 71
}
prumer = sum(grades.values()) / len(grades)
print(prumer)


#Reseni 8
body = list(grades.values())
print(body)


#Reseni 9
predmety = list(grades.keys())
print(predmety)


#Reseni 10
bodyBiologie = grades.get('Biology', 0)
print(bodyBiologie)


#Reseni 11
maFyziku = 'Physics' in grades
ma100 = 100 in grades.values()
print(maFyziku, ma100)


#Reseni 12
trida = [
    {'jmeno': 'Jana', 'znamky': [1, 2, 1]},
    {'jmeno': 'Petr', 'znamky': [3, 2]}
]
prvniZnamkaPetra = trida[1]['znamky'][0]
print(prvniZnamkaPetra)


#Reseni 13
trida.append({'jmeno': 'Eva', 'znamky': [2, 2]})

print(trida)

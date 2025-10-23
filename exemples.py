#commentaire une seule ligne
"""
commentaire sur plusieurs lignes
"""
age=12
chaine="oumeima"
if age<13:
    print("enfant")
elif 13<=age<=18:
    print("adolescent")
else:
    print("adulte")
entier=34
print(type(entier))
decimal=3.15
boo=5>10
print(boo)
chaine1="Bonjour"

liste_chaine=["pomme", "banane", "orange"]
tuple_exemple=(10.5,20.5)
dictionnaire={"nom":"Alice", "age":30}
set_exemple={}
set_exemple2={1, 2, 3,1}
print(set_exemple)
print(type(dictionnaire))
print(type(set_exemple))

a=4
b=5
addition=a+b
puissance=a**b
print(addition,puissance)

chaine1="Bonjour"
chaine2="3IA4"
concat=chaine1+chaine2
longuer=len(concat)
sous_chaine=concat[0:7]
print(concat,longuer,sous_chaine)

liste= [1, 2, 3]
liste2= [4, 5, 6]
liste.append(4)
liste.remove(2)
print(liste[1])
liste_finale=liste+liste2
print( liste_finale)

dictionnaire2={"ville":"Paris", "code_postal":75000}
print(dictionnaire2["ville"])
dictionnaire2["pays"]="France"
print(dictionnaire2)

for n in liste:
    print(n*2)

c=1
while c<=5:
    print(c)
    if(c>3):
        break
    c+=1
def somme(a, b):
    return a + b
def somme2(a:int,b:int)->int:
    return a + b

print(somme2(1,2))
print(somme2("bonjour", "tout le monde"))
def greeting(name: str="X") -> str:
    return f"Bonjour, {name}!"

print(greeting())
print(greeting("Alice"))

nom=input("Entrez votre nom: ")
age=int(input("Entrez votre age: "))

print(f"Bonjour {nom}, vous avez {age} ans.")

try:
    n=int(input("Entrez un nombre entier: "))
    res=10/n
    print(res)
except ValueError:
    print("Veuillez entrer un nombre entier valide.")
except ZeroDivisionError:
    print("Erreur : Division par zéro.")
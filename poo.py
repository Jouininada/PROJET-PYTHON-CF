class Vehicule:
    def __init__(self,matricule,annee,kilometrage,
                 numero_serie):
        self.matricule=matricule
        self._annee=annee
        self.__kilometrage=kilometrage
        self.numero_serie=numero_serie
    @property
    def kilometrage(self):
        return self.__kilometrage
    @kilometrage.setter
    def kilometrage(self,nouvelle_value):
        self.__kilometrage=nouvelle_value
    def __str__(self):
        return f"les informations de cet objet est {self.matricule} et {self._annee}"    
    def afficher_numero(self):
        return f"{self.numero_serie}"
    
class Voiture(Vehicule):
    def __init__(self, matricule, annee, 
                 kilometrage, numero_serie,color):
        super().__init__(matricule, annee, 
                         kilometrage, numero_serie)
        self.color=color

v=Vehicule("133",2001,230000,"TU789")
voiture=Voiture("133",2001,230000,"TU79","rouge")
print(voiture.afficher_numero())
print(v.afficher_numero())
print(v)
print(v.matricule)
print(v._annee)
print(v._Vehicule__kilometrage)

print(v.__dict__)
print(v.__class__)
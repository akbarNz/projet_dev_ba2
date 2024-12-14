import json
import re
from Oeuvre import Oeuvre

class Collection:
    def __init__(self, nom):
        self.nom = nom
        self.oeuvres = []

    def ajouter_oeuvre(self, oeuvre):
        if oeuvre not in self.oeuvres:
            self.oeuvres.append(oeuvre)

    def __str__(self):
        oeuvres_titres = ', '.join([oeuvre.titre for oeuvre in self.oeuvres])
        return f"Collection: {self.nom} avec les œuvres: [{oeuvres_titres}]"

    def to_dict(self):
        return {
            "nom": self.nom,
            "oeuvres": [oeuvre.titre for oeuvre in self.oeuvres]
        }

    @staticmethod
    def from_dict(data, oeuvres):
        collection = Collection(data["nom"])
        for titre in data["oeuvres"]:
            oeuvre = next((o for o in oeuvres if o.titre == titre), None)
            if oeuvre:
                collection.ajouter_oeuvre(oeuvre)
        return collection
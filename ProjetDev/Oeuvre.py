import json
import re


class Oeuvre:
    def __init__(self, titre, description, artiste=None, couleur_dominante=None, courant=None):
        self.titre = titre
        self.description = description
        self.artiste = artiste
        self.couleur_dominante = couleur_dominante
        self.courant = courant

    def __str__(self):
        artiste_info = self.artiste.identite if self.artiste else "Inconnu"
        return (f"Oeuvre: {self.titre}, Artiste: {artiste_info}, Description: {self.description}, "
                f"Couleur Dominante: {self.couleur_dominante}, Courant: {self.courant}")

    def to_dict(self):
        return {
            "titre": self.titre,
            "description": self.description,
            "artiste": self.artiste.identite if self.artiste else None,
            "couleur_dominante": self.couleur_dominante,
            "courant": self.courant
        }
    

    @staticmethod
    def from_dict(data, artistes):
        artiste = next((a for a in artistes if a.identite == data["artiste"]), None)
        return Oeuvre(
            titre=data["titre"],
            description=data["description"],
            artiste=artiste,
            couleur_dominante=data.get("couleur_dominante"),
            courant=data.get("courant")
        )
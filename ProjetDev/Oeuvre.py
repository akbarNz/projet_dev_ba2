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
    
    def assigner_artiste(self, artiste):
        if self.artiste is None:
            self.artiste = artiste
            print(f"Artiste '{artiste.identite}' assigné à l'œuvre '{self.titre}'.")
        else:
            print(f"L'œuvre '{self.titre}' a déjà un artiste assigné : {self.artiste.identite}.")


    @staticmethod
    def from_dict(data, artistes):
        # Recherche l'artiste associé par son identité
        artiste = next((a for a in artistes if a.identite == data.get('artiste')), None)
        return Oeuvre(
            data['titre'],
            data['description'],
            artiste,
            data.get('couleur_dominante'),
            data.get('courant')
        )
# art_management.py

from datetime import datetime

class Artiste:
    def __init__(self, identite, biographie, date_naissance, date_deces=None):
        self.identite = identite
        self.biographie = biographie
        self.date_naissance = convertir_date(date_naissance)
        self.date_deces = convertir_date(date_deces) if date_deces else None
        self.oeuvres = []
    def __str__(self):
        return f"Artiste: {self.identite}, Bio: {self.biographie}"


class Oeuvre:
    def __init__(self, titre, description, couleur_dominante,artiste=None):
        self.titre = titre
        self.description = description
        self.artiste = artiste
        if artiste:
            artiste.oeuvre.append(self.titre)
        self.couleur_dominante = couleur_dominante

    def __str__(self):
        artiste_info = self.artiste.identite if self.artiste else "Inconnu"
        return f"Oeuvre: {self.titre}, Artiste: {artiste_info}, Description: {self.description}, Couleur Dominante: {self.couleur_dominante}"


class Collection:
    def __init__(self, nom):
        self.nom = nom
        self.oeuvres = []

        def ajouter_oeuvre(self, oeuvre):
            self.oeuvres.append(oeuvre)


    def __str__(self):
        oeuvres_titres = ', '.join([oeuvre.titre for oeuvre in self.oeuvres])
        return f"Collection: {self.nom} avec les œuvres: [{oeuvres_titres}]"


class Exposition:
    def __init__(self, nom, date_debut, date_fin, collection):
        self.nom = nom
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.collection = collection

    def __str__(self):
        return f"Exposition: {self.nom}, du {self.date_debut} au {self.date_fin}, Collection: {self.collection.nom}"

# Fonctions utilitaires pour gérer la logique
def trouver_artiste_par_nom(artistes, identite):
    for artiste in artistes:
        if artiste.identite.lower() == identite.lower():
            return artiste
    return None

def trouver_oeuvre_par_titre(oeuvres, titre):
    for oeuvre in oeuvres:
        if oeuvre.titre.lower() == titre.lower():
            return oeuvre
    return None

def convertir_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("Format de date incorrect. Utilisez AAAA-MM-JJ.")
        return None

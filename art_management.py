from datetime import datetime
import json


class Artiste:
    def __init__(self, identite, biographie, date_naissance, date_deces=None):
        self.identite = identite
        self.biographie = biographie
        self.date_naissance = convertir_date(date_naissance)
        self.date_deces = convertir_date(date_deces) if date_deces else None

    def __str__(self):
        return f"Artiste: {self.identite}, Bio: {self.biographie}"

    def to_dict(self):
        return {
            "identite": self.identite,
            "biographie": self.biographie,
            "date_naissance": self.date_naissance.strftime("%Y-%m-%d") if self.date_naissance else None,
            "date_deces": self.date_deces.strftime("%Y-%m-%d") if self.date_deces else None
        }

    @staticmethod
    def from_dict(data):
        return Artiste(
            data["identite"],
            data["biographie"],
            data["date_naissance"],
            data["date_deces"]
        )


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


def convertir_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None


def trouver_artiste_par_nom(artistes, identite):
    return next((artiste for artiste in artistes if artiste.identite.lower() == identite.lower()), None)


def trouver_oeuvre_par_titre(oeuvres, titre):
    return next((oeuvre for oeuvre in oeuvres if oeuvre.titre.lower() == titre.lower()), None)


def sauvegarder_donnees(fichier, artistes, oeuvres, collections):
    data = {
        "artistes": [artiste.to_dict() for artiste in artistes],
        "oeuvres": [oeuvre.to_dict() for oeuvre in oeuvres],
        "collections": [collection.to_dict() for collection in collections]
    }
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def charger_donnees(fichier):
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            data = json.load(f)
            artistes = [Artiste.from_dict(a) for a in data["artistes"]]
            oeuvres = [Oeuvre.from_dict(o, artistes) for o in data["oeuvres"]]
            collections = [Collection.from_dict(c, oeuvres) for c in data["collections"]]
            return artistes, oeuvres, collections
    except FileNotFoundError:
        return [], [], []

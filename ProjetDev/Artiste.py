import json
import re
from Oeuvre import Oeuvre
from Collection import Collection

class Artiste:
    def __init__(self, identite, biographie, date_naissance, date_deces=None):
        self.identite = identite
        self.biographie = biographie
        self.date_naissance = date_naissance
        self.date_deces = date_deces

    def __str__(self):
        return (f"Artiste: {self.identite}, Biographie: {self.biographie}, "
                f"Date de naissance: {self.date_naissance}, Date de décès: {self.date_deces or 'N/A'}")

    def to_dict(self):
        return {
            "identite": self.identite,
            "biographie": self.biographie,
            "date_naissance": self.date_naissance,
            "date_deces": self.date_deces
        }

    @staticmethod
    def from_dict(data):
        return Artiste(
            data["identite"],
            data["biographie"],
            data["date_naissance"],
            data.get("date_deces")
        )

    def modifier(self, identite=None, biographie=None, date_naissance=None, date_deces=None):
        if identite:
            self.identite = identite
        if biographie:
            self.biographie = biographie
        if date_naissance:
            self.date_naissance = date_naissance
        if date_deces:
            self.date_deces = date_deces


def valider_format_date(date_str):
    """Valide et conserve la date au format original, sans ajouter de zéros."""
    if not date_str:
        return True, None

    match = re.match(r"(\d{1,4})-(\d{1,2})-(\d{1,2})$", date_str)
    if not match:
        return False, None

    annee, mois, jour = match.groups()

    if not (1 <= int(annee) <= 9999):
        return False, None
    if not (1 <= int(mois) <= 12):
        return False, None
    if not (1 <= int(jour) <= 31):
        return False, None

    return True, date_str


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
            contenu = f.read().strip()
            if not contenu:
                return [], [], []
            data = json.loads(contenu)
            artistes = [Artiste.from_dict(a) for a in data.get("artistes", [])]
            oeuvres = [Oeuvre.from_dict(o, artistes) for o in data.get("oeuvres", [])]
            collections = [Collection.from_dict(c, oeuvres) for c in data.get("collections", [])]
            return artistes, oeuvres, collections
    except FileNotFoundError:
        return [], [], []
    except json.JSONDecodeError as e:
        print(f"Erreur de lecture JSON : {e}")
        return [], [], []

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


def trouver_artiste_par_nom(artistes, nom):
    return next((artiste for artiste in artistes if artiste.identite.lower() == nom.lower()), None)

def trouver_oeuvre_par_titre(oeuvres, titre):
    return next((oeuvre for oeuvre in oeuvres if oeuvre.titre.lower() == titre.lower()), None)

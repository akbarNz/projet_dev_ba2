class Collection:
    def __init__(self, nom):
        self._nom = nom
        self._oeuvres = []

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, nom):
        self._nom = nom

    @property
    def oeuvres(self):
        return self._oeuvres

    def ajouter_oeuvre(self, oeuvre):
        if oeuvre not in self._oeuvres:
            self._oeuvres.append(oeuvre)

    def __str__(self):
        oeuvres_titres = ', '.join([oeuvre.titre for oeuvre in self._oeuvres])
        return f"Collection: {self._nom} avec les oeuvres: [{oeuvres_titres}]"

    def to_dict(self):
        return {
            "nom": self._nom,
            "oeuvres": [oeuvre.titre for oeuvre in self._oeuvres]
        }

    def enlever_oeuvre(self, oeuvre):
        if oeuvre in self._oeuvres:
            self._oeuvres.remove(oeuvre)

    @staticmethod
    def from_dict(data, oeuvres):
        collection = Collection(data["nom"])
        for titre in data["oeuvres"]:
            oeuvre = next((o for o in oeuvres if o.titre == titre), None)
            if oeuvre:
                collection.ajouter_oeuvre(oeuvre)
        return collection

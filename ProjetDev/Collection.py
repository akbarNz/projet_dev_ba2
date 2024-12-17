from operator import attrgetter

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
    # nouveau

    def est_vide(self):
        """collection vide.Renvoie True si vide, False sinon"""
        return len(self.oeuvres) == 0
    
    def tri_col(self, date_apparition, titre):
        """trie la collection d'oeuvres par la date d'apparition (majeure) tri par defaut et/ou titre (mineure)"""
        if date_apparition:
            # tri par date d'apparition des oeuvres
            self._tri_oeuvres_apparition()
            # tri par titre
            if titre:
                self._tri_oeuvres_titre()
        elif titre:
            # tri oeuvre par titre
            self._tri_oeuvres_titre()
        else:
            # tri par date d'apparition defaut
            self._tri_oeuvres_apparition()
    
    def _tri_oeuvres_apparition(self):
        """Trier les oeuvres par le date d'apparition"""
        self.oeuvres.sort(key=attrgetter('date_apparition'))
    
    def _tri_oeuvres_titre(self):
        """Trier les oeuvres par leur titre"""
        self.oeuvres.sort(key=attrgetter('titre'))

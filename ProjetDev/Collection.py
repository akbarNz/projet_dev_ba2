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
    
    
    def tri_oeuvres_apparition(self):
        """Trier les oeuvres par le date d'apparition. Renvoie une str"""
        self.oeuvres.sort(key=attrgetter('date_apparition'))
        tmp = {}

        for o in self.oeuvres:
            if o.date_apparition not in tmp:
                tmp[o.date_apparition] = [o.titre]
            else:
                tmp[o.date_apparition].append(o.titre)
        
        s = "Les oeuvres triés par date d'apparition.\n"
        for k in tmp.keys():
            s += f"{k} : {tmp[k]}\n"
        return s
    
    def tri_oeuvres_titre(self):
        """Trier les oeuvres par leur titre. Renvoie une str"""
        self.oeuvres.sort(key=attrgetter('titre'))

        tmp = {}

        for o in self.oeuvres:
            if o.titre not in tmp:
                tmp[o.titre] = o.description
            else:
                tmp[o.titre].append(o.description)
        
        s = "Les oeuvres triés par titre.\n"
        for k in tmp.keys():
            s += f"{k} : {tmp[k]}\n"
        return s
    
    def tri_oeuvres_couleur_dominante(self):
        """Triez les oeuvres par la couleur dominante. renvoie une str de la representation du tri"""
        self.oeuvres.sort(key=attrgetter('couleur_dominante'))
        tmp = {}

        for o in self.oeuvres:
            if o.couleur_dominante not in tmp:
                tmp[o.couleur_dominante] = [o.titre]
            else:
                tmp[o.couleur_dominante].append(o.titre)
        
        s = "Les oeuvres triés par couleur dominante.\n"
        for k in tmp.keys():
            s += f"{k} : {tmp[k]}\n"
        return s
    
    def tri_par_courant(self):
        """trier les oeuvres par courant. renvoie une str de la representation du tri"""
        self.oeuvres.sort(key=attrgetter('courant'))
        tmp = {}

        for o in self.oeuvres:
            if o.courant not in tmp:
                tmp[o.courant] = [o.titre]
            else:
                tmp[o.courant].append(o.titre)
        
        s = "Les oeuvres triés par courant.\n"
        for k in tmp.keys():
            s += f"{k} : {tmp[k]}\n"
        return s
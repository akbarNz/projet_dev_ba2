class Exposition:
    def __init__(self, collections, date, invités=[]):
        self.collections = collections
        self.date = date
        self.invités = list(invités)

    def ajouter_invités(self, liste_invités):
        ajoutés = 0
        for invité in liste_invités:
            if invité not in self.invités:
                self.invités.append(invité)
                ajoutés += 1
        print(f"{ajoutés} invités ajoutés.")

    def enlever_invités(self, liste_invités):
        enlevés = 0
        for invité in liste_invités:
            if invité in self.invités:
                self.invités.remove(invité)
                enlevés += 1
        print(f"{enlevés} invités enlevés.")

    def supprimer_collection(self, collection):
        if collection in self.collections:
            self.collections.remove(collection)
            print(f"La collection '{collection.nom}' a été supprimée de l'exposition du {self.date}.")
        else:
            print(f"La collection '{collection.nom}' n'est pas présente dans cette exposition.")

    def to_dict(self):
        return {
            "collections": [col.nom for col in self.collections],
            "date": self.date,
            "invités": self.invités
        }

    @staticmethod
    def from_dict(data, collections):
        collections_expo = [next((c for c in collections if c.nom == nom), None) for nom in data["collections"]]
        return Exposition(collections_expo, data["date"], data["invités"])

    def supprimer_toutes_les_collections(self):
        self.collections.clear()
        print(f"Toutes les collections ont été supprimées de l'exposition du {self.date}.")

    def __str__(self):
        invités_str = ', '.join(self.invités)
        return f"Exposition le {self.date}, Collections: {[col.nom for col in self.collections]}, Invités: {invités_str if invités_str else 'Aucun'}"

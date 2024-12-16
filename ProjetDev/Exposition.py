class Exposition:
    def __init__(self, collections, date, invites=[]):
        self.collections = collections
        self.date = date
        self.invites = list(invites)

    def __str__(self):
        invites_str = ', '.join(self.invites)
        return f"Exposition le {self.date}, Collections: {[col.nom for col in self.collections]}, Invites: {invites_str if invites_str else 'Aucun'}"

    def ajouter_invites(self, liste_invites):
        for invite in liste_invites:
            if invite not in self.invites:
                self.invites.append(invite)

    def enlever_invites(self, liste_invites):
        for invite in liste_invites:
            if invite in self.invites:
                self.invites.remove(invite)

    def supprimer_collection(self, collection):
        if collection in self.collections:
            self.collections.remove(collection)

    def to_dict(self):
        return {
            "collections": [col.nom for col in self.collections],
            "date": self.date,
            "invites": self.invites
        }

    @staticmethod
    def from_dict(data, collections):
        collections_expo = [next((c for c in collections if c.nom == nom), None) for nom in data["collections"]]
        return Exposition(collections_expo, data["date"], data["invites"])

    def supprimer_toutes_les_collections(self):
        self.collections.clear()

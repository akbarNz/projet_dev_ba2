from datetime import datetime

class Artiste:
    def __init__(self, identite, bio, date_naissance, date_deces=None):
        self.identite = identite  # Nom complet (ex: "Prénom Nom")
        self.bio = bio
        self.date_naissance = self._convertir_date(date_naissance)
        self.date_deces = self._convertir_date(date_deces) if date_deces else None
        self.oeuvres = []

    def _convertir_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Format de date incorrect. Utilisez AAAA-MM-JJ.")
            return None

    def __str__(self):
        return f"Artiste: {self.identite}, Bio: {self.bio}"

class Oeuvre:
    def __init__(self, titre, description, artiste=None):
        self.titre = titre
        self.description = description
        self.artiste = artiste
        if artiste:
            artiste.oeuvres.append(self)

    def __str__(self):
        artiste_info = self.artiste.identite if self.artiste else "Inconnu"
        return f"Oeuvre: {self.titre}, Artiste: {artiste_info}, Description: {self.description}"

class Collection:
    def __init__(self, nom):
        self.nom = nom
        self.oeuvres = []

    def ajouter_oeuvre(self, oeuvre):
        self.oeuvres.append(oeuvre)
        print(f"Oeuvre '{oeuvre.titre}' ajoutée à la collection '{self.nom}'.")

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

def creer_ou_trouver_artiste():
    identite = input("Entrez le nom complet de l'artiste (Prénom Nom): ")
    
    # Vérifier l'existence de l'artiste avec son nom complet
    for artiste in artistes:
        if artiste.identite.lower() == identite.lower():
            return artiste

    # Artiste non trouvé, proposer de le créer
    print("Artiste non trouvé.")
    if input("Voulez-vous créer cet artiste ? (oui/non): ").lower() == "oui":
        bio = input("Biographie: ")
        date_naissance = input("Date de naissance (AAAA-MM-JJ): ")
        date_deces = input("Date de décès (si applicable, sinon laisser vide): ") or None
        artiste = Artiste(identite, bio, date_naissance, date_deces)
        artistes.append(artiste)
        return artiste
    return None

def ajouter_ou_trouver_oeuvre():
    titre = input("Entrez le titre de l'œuvre à rechercher ou créer: ")
    for oeuvre in oeuvres:
        if oeuvre.titre.lower() == titre.lower():
            return oeuvre
    if input("Oeuvre non trouvée. Voulez-vous la créer ? (oui/non): ").lower() == "oui":
        description = input("Description de l'œuvre: ")
        artiste = creer_ou_trouver_artiste()
        if artiste:
            oeuvre = Oeuvre(titre, description, artiste)
            oeuvres.append(oeuvre)
            return oeuvre
    return None

def main():
    global artistes, oeuvres, collections
    artistes = []
    oeuvres = []
    collections = []

    while True:
        choix = input("Voulez-vous gérer un 'artiste', une 'oeuvre', une 'collection', une 'exposition' ou 'quitter' ? ")
        if choix.lower() == 'quitter':
            break
        elif choix.lower() == 'artiste':
            artiste = creer_ou_trouver_artiste()
            if artiste:
                print(artiste)
        elif choix.lower() == 'oeuvre':
            oeuvre = ajouter_ou_trouver_oeuvre()
            if oeuvre:
                print(oeuvre)
        elif choix.lower() == 'collection':
            nom_collection = input("Nom de la collection à créer ou afficher: ")
            collection = next((c for c in collections if c.nom.lower() == nom_collection.lower()), None)
            if not collection:
                collection = Collection(nom_collection)
                collections.append(collection)
            while True:
                ajout = input("Voulez-vous ajouter une oeuvre à cette collection ? (oui/non): ")
                if ajout.lower() == 'non':
                    break
                oeuvre = ajouter_ou_trouver_oeuvre()
                if oeuvre:
                    collection.ajouter_oeuvre(oeuvre)
            print(collection)
        elif choix.lower() == 'exposition':
            nom_collection = input("Nom de la collection pour l'exposition: ")
            collection = next((c for c in collections if c.nom.lower() == nom_collection.lower()), None)
            if collection:
                nom_expo = input("Nom de l'exposition: ")
                date_debut = input("Date de début (AAAA-MM-JJ): ")
                date_fin = input("Date de fin (AAAA-MM-JJ): ")
                exposition = Exposition(nom_expo, date_debut, date_fin, collection)
                print(exposition)
            else:
                print("Collection non trouvée.")

main()

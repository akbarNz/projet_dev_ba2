class Artiste:
    def __init__(self, nom, prenom, bio, date_naissance, date_deces=None):
        self.nom = nom
        self.prenom = prenom
        self.bio = bio
        self.date_naissance = date_naissance
        self.date_deces = date_deces
        self.oeuvres = []

    def __str__(self):
        return f"Artiste: {self.prenom} {self.nom}, Bio: {self.bio}"

class Oeuvre:
    def __init__(self, titre, description, artiste=None):
        self.titre = titre
        self.description = description
        self.artiste = artiste
        if artiste:
            artiste.oeuvres.append(self)

    def __str__(self):
        artiste_info = f"{self.artiste.prenom} {self.artiste.nom}" if self.artiste else "Inconnu"
        return f"Oeuvre: {self.titre}, Artiste: {artiste_info}, Description: {self.description}"

class Collection:
    def __init__(self, nom):
        self.nom = nom
        self.oeuvres = []

    def ajouter_oeuvre(self, oeuvre):
        self.oeuvres.append(oeuvre)
        print(f"Oeuvre '{oeuvre.titre}' ajoutée à la collection '{self.nom}'.")

    def __str__(self):
        return f"Collection: {self.nom} avec les œuvres: {[oeuvre.titre for oeuvre in self.oeuvres]}"

class Exposition:
    def __init__(self, nom, date_debut, date_fin, collection):
        self.nom = nom
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.collection = collection

    def __str__(self):
        return f"Exposition: {self.nom}, du {self.date_debut} au {self.date_fin}, Collection: {self.collection.nom}"

def creer_ou_trouver_artiste():
    nom = input("Entrez le nom complet de l'artiste à rechercher ou créer: ")
    for artiste in artistes:
        if artiste.nom.lower() == nom.lower():
            return artiste
    print("Artiste non trouvé.")
    if input("Voulez-vous créer cet artiste ? (oui/non): ").lower() == "oui":
        prenom = input("Prénom de l'artiste: ")
        bio = input("Biographie: ")
        date_naissance = input("Date de naissance (AAAA-MM-JJ): ")
        date_deces = input("Date de décès (si applicable, sinon laisser vide): ") or None
        artiste = Artiste(nom, prenom, bio, date_naissance, date_deces)
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
        oeuvre = Oeuvre(titre, description, artiste)
        oeuvres.append(oeuvre)
        return oeuvre
    return None

artistes = []
oeuvres = []
collections = []

def main():
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

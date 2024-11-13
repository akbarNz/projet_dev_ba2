# main_interface.py

from art_management import Artiste, Oeuvre, Collection, Exposition, trouver_artiste_par_nom, trouver_oeuvre_par_titre

def creer_ou_trouver_artiste(artistes):
    identite = input("Entrez le nom complet de l'artiste (Prénom Nom): ")
    artiste = trouver_artiste_par_nom(artistes, identite)
    if artiste:
        return artiste

    print("Artiste non trouvé.")
    if input("Voulez-vous créer cet artiste ? (oui/non): ").lower() == "oui":
        bio = input("Biographie: ")
        date_naissance = input("Date de naissance (AAAA-MM-JJ): ")
        date_deces = input("Date de décès (si applicable, sinon laisser vide): ") or None
        artiste = Artiste(identite, bio, date_naissance, date_deces)
        artistes.append(artiste)
        return artiste
    return None

def ajouter_ou_trouver_oeuvre(artistes, oeuvres):
    titre = input("Entrez le titre de l'œuvre à rechercher ou créer: ")
    oeuvre = trouver_oeuvre_par_titre(oeuvres, titre)
    if oeuvre:
        return oeuvre

    if input("Oeuvre non trouvée. Voulez-vous la créer ? (oui/non): ").lower() == "oui":
        description = input("Description de l'œuvre: ")
        artiste = creer_ou_trouver_artiste(artistes)
        if artiste:
            oeuvre = Oeuvre(titre, description, artiste)
            oeuvres.append(oeuvre)
            return oeuvre
    return None

def main():
    artistes = []
    oeuvres = []
    collections = []

    while True:
        choix = input("Voulez-vous gérer un 'artiste', une 'oeuvre', une 'collection', une 'exposition' ou 'quitter' ? ")
        if choix.lower() == 'quitter':
            break
        elif choix.lower() == 'artiste':
            artiste = creer_ou_trouver_artiste(artistes)
            if artiste:
                print(artiste)
        elif choix.lower() == 'oeuvre':
            oeuvre = ajouter_ou_trouver_oeuvre(artistes, oeuvres)
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
                oeuvre = ajouter_ou_trouver_oeuvre(artistes, oeuvres)
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

if __name__ == "__main__":
    main()

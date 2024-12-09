from art_management import (
    charger_donnees, sauvegarder_donnees,
    Artiste, Oeuvre, Collection,
    trouver_artiste_par_nom, trouver_oeuvre_par_titre
)


def creer_ou_trouver_artiste(artistes):
    identite = input("Entrez le nom complet de l'artiste (Prénom Nom): ")
    artiste = trouver_artiste_par_nom(artistes, identite)
    if artiste:
        print(f"Artiste trouvé : {artiste}")
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
        print(f"Oeuvre trouvée : {oeuvre}")
        return oeuvre

    if input("Oeuvre non trouvée. Voulez-vous la créer ? (oui/non): ").lower() == "oui":
        description = input("Description de l'œuvre: ")
        artiste = creer_ou_trouver_artiste(artistes)
        if artiste:
            oeuvre = Oeuvre(titre, description, artiste)
            oeuvres.append(oeuvre)
            return oeuvre
    return None


def gerer_collection(artistes, oeuvres, collections):
    nom_collection = input("Nom de la collection à créer ou afficher: ")
    collection = next((c for c in collections if c.nom.lower() == nom_collection.lower()), None)
    if not collection:
        collection = Collection(nom_collection)
        collections.append(collection)

    while True:
        ajout = input("Voulez-vous ajouter une œuvre à cette collection ? (oui/non): ")
        if ajout.lower() == 'non':
            break
        oeuvre = ajouter_ou_trouver_oeuvre(artistes, oeuvres)
        if oeuvre:
            collection.ajouter_oeuvre(oeuvre)
    print(collection)


def main():
    fichier_donnees = "donnees.json"
    artistes, oeuvres, collections = charger_donnees(fichier_donnees)

    while True:
        choix = input("Voulez-vous gérer un 'artiste', une 'œuvre', une 'collection' ou 'quitter' ? ")
        if choix.lower() == 'quitter':
            break
        elif choix.lower() == 'artiste':
            creer_ou_trouver_artiste(artistes)
        elif choix.lower() == 'œuvre':
            ajouter_ou_trouver_oeuvre(artistes, oeuvres)
        elif choix.lower() == 'collection':
            gerer_collection(artistes, oeuvres, collections)

    sauvegarder_donnees(fichier_donnees, artistes, oeuvres, collections)


if __name__ == "__main__":
    main()

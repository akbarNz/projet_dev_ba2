from Artiste import ( Artiste,
    charger_donnees, sauvegarder_donnees,trouver_artiste_par_nom, trouver_oeuvre_par_titre, valider_format_date
)
from Oeuvre import Oeuvre
from Collection import Collection
from Exposition import Exposition

def demander_date_str(message, obligatoire=False):
    while True:
        date_str = input(message).strip()
        if not date_str and not obligatoire:
            return None
        if valider_format_date(date_str):
            return date_str
        print("Format de date invalide. Veuillez utiliser le format AAAA-MM-JJ.")


def creer_ou_trouver_artiste(artistes):
    identite = input("Entrez le nom complet de l'artiste (Prénom Nom): ").strip()
    artiste = trouver_artiste_par_nom(artistes, identite)
    
    if artiste:
        print(f"Artiste trouvé : {artiste}")
        action = input("Voulez-vous 'voir' l'artiste ou 'modifier' ses informations ? (voir/modifier): ").strip().lower()
        if action == 'modifier':
            identite = input("Modifier nom et prénom (laisser vide pour ne pas modifier)").strip()
            biographie = input("Nouvelle biographie (laisser vide pour ne pas modifier): ").strip()
            date_naissance = input("Nouvelle date de naissance (AAAA-MM-JJ, laisser vide pour ne pas modifier): ").strip()
            date_deces = input("Nouvelle date de décès (AAAA-MM-JJ, laisser vide pour ne pas modifier): ").strip()
            artiste.modifier(biographie, date_naissance, date_deces)
            print(f"Artiste modifié : {artiste}")
        return artiste
    else:
        print("Artiste non trouvé.")
        if input("Voulez-vous créer cet artiste ? (oui/non): ").strip().lower() == "oui":
            bio = input("Biographie: ").strip()
            date_naissance = input("Date de naissance (AAAA-MM-JJ): ").strip()
            date_deces = input("Date de décès (si applicable, sinon laisser vide): ").strip() or None
            artiste = Artiste(identite, bio, date_naissance, date_deces)
            artistes.append(artiste)
            return artiste
    return None

def ajouter_oeuvres_multiples_a_collection(oeuvres, collection):
    print("Choisissez un ou plusieurs critères pour ajouter des œuvres à la collection (séparez par des virgules):")
    print("1. Artiste")
    print("2. Courant artistique")
    print("3. Couleur dominante")
    choix_utilisateur = input("Votre choix (ex: 1, 2) : ").strip()

    critere_mapping = {
        '1': ('artiste', 'identite'),
        '2': ('courant', 'courant'),
        '3': ('couleur_dominante', 'couleur_dominante')
    }
    choixs = choix_utilisateur.split(',')
    criteres = []

    for choix in choixs:
        choix = choix.strip()
        if choix in critere_mapping:
            nom_critere, attr = critere_mapping[choix]
            valeur = input(f"Entrez {nom_critere} : ").strip()
            criteres.append((attr, valeur.lower()))

    oeuvres_a_ajouter = [oeuvre for oeuvre in oeuvres if all(getattr(oeuvre, attr, '').lower() == val for attr, val in criteres)]
    
    for oeuvre in oeuvres_a_ajouter:
        collection.ajouter_oeuvre(oeuvre)
        print(f"'{oeuvre.titre}' ajoutée à la collection '{collection.nom}'.")
    if oeuvres_a_ajouter:
        print(f"{len(oeuvres_a_ajouter)} œuvres ajoutées à la collection.")
    else:
        print("Aucune œuvre trouvée avec les critères spécifiés.")



def ajouter_ou_trouver_oeuvre(artistes, oeuvres):
    titre = input("Entrez le titre de l'œuvre à rechercher ou créer: ").strip()
    oeuvre = trouver_oeuvre_par_titre(oeuvres, titre)
    if oeuvre:
        print(f"Œuvre trouvée : {oeuvre}")
        if oeuvre.artiste is None:
            if input("Cette œuvre n'a pas d'artiste assigné. Voulez-vous en ajouter un ? (oui/non) : ").strip().lower() == "oui":
                artiste = creer_ou_trouver_artiste(artistes)
                if artiste:
                    oeuvre.assigner_artiste(artiste)
        return oeuvre

    if input("Œuvre non trouvée. Voulez-vous la créer ? (oui/non): ").strip().lower() == "oui":
        description = input("Description de l'œuvre: ").strip()
        couleur_dominante = input("Couleur dominante: ").strip()
        courant = input("Courant artistique: ").strip()
        choix_artiste = input("Artiste connu ? (oui/non): ")
        if choix_artiste == "non":
            artiste = None 
        else:    
            artiste = creer_ou_trouver_artiste(artistes)
        oeuvre = Oeuvre(
            titre=titre,
            description=description,
            artiste=artiste,
            couleur_dominante=couleur_dominante,
            courant=courant
        )
        oeuvres.append(oeuvre)
        return oeuvre
    return None

def afficher_collections_disponibles(collections):
    if not collections:
        print("Aucune collection disponible.")
        return None
    print("Collections disponibles :")
    for idx, collection in enumerate(collections, start=1):
        print(f"{idx}. {collection.nom}")
    return collections

def choisir_collection(collections):
    collections = afficher_collections_disponibles(collections)
    if not collections:
        return None
    choix = input("Choisissez une collection par numéro ou entrez le nom : ").strip().lower()
    try:
        # Permet de choisir par numéro, en supposant que l'utilisateur peut saisir un indice basé sur l'affichage précédent
        return collections[int(choix) - 1]
    except (ValueError, IndexError):
        # Permet de choisir par nom si l'entrée n'est pas un nombre ou hors de l'index
        return next((col for col in collections if col.nom.lower() == choix), None)

def gerer_collection(artistes, oeuvres, collections):
    choix_collection = input("Voulez-vous 'créer' une nouvelle collection ou 'utiliser' une collection existante ? (créer/utiliser) : ").strip().lower()
    if choix_collection == 'creer' or choix_collection == 'créer':
        nom_collection = input("Entrez le nom de la nouvelle collection : ").strip()
        collection = Collection(nom_collection)
        collections.append(collection)
        print(f"Nouvelle collection créée : {nom_collection}")
    elif choix_collection == 'utiliser':
        collection = choisir_collection(collections)
        if not collection:
            print("Collection non trouvée ou choix invalide.")
            return
        nom_collection = collection.nom  # Utiliser le nom de la collection existante
        print(f"Utilisation de la collection existante : {nom_collection}")
    else:
        print("Choix invalide.")
        return

    while True:
        action = input("Voulez-vous ajouter 'une' oeuvre ou 'plusieurs' oeuvres à la collection ? (une/plusieurs) : ").strip().lower()
        if action == 'une':
            oeuvre = ajouter_ou_trouver_oeuvre(artistes, oeuvres)
            if oeuvre:
                collection.ajouter_oeuvre(oeuvre)
                print(f"L'oeuvre '{oeuvre.titre}' a été ajoutée à la collection '{nom_collection}'.")
        elif action == 'plusieurs':
            ajouter_oeuvres_multiples_a_collection(oeuvres, collection)
        else:
            print("Choix invalide. Veuillez choisir 'une' ou 'plusieurs'.")
            continue
        
        encore = input("Voulez-vous ajouter d'autres œuvres à cette collection ? (oui/non) : ").strip().lower()
        if encore != 'oui':
            break

def gerer_expositions(collections, expositions):
    choix = input("Voulez-vous 'créer' une nouvelle exposition, 'modifier' une exposition existante, ou 'voir' les expositions existantes ? (créer/modifier/voir) : ").strip().lower()
    if choix == 'créer' or choix == 'creer':
        date = input("Entrez la date de l'exposition (AAAA-MM-JJ): ")
        collections_exposees = choisir_collections(collections)
        exposition = Exposition(collections_exposees, date)
        gerer_invites(exposition)
        expositions.append(exposition)
        print(f"Exposition prévue le {date} créée.")
    elif choix == 'modifier':
        date = input("Entrez la date de l'exposition à modifier (AAAA-MM-JJ): ")
        exposition = next((expo for expo in expositions if expo.date == date), None)
        if exposition:
            gerer_invites(exposition)
        else:
            print("Aucune exposition trouvée pour cette date.")
    elif choix == 'voir':
        if expositions:
            for expo in expositions:
                print(expo)
        else:
            print("Aucune exposition existante.")
    else:
        print("Choix invalide.")
        
def gerer_invites(exposition):
    while True:
        action = input("Voulez-vous 'ajouter' des invités, 'enlever' des invités, ou 'terminer' ? (ajouter/enlever/terminer) ").strip().lower()
        if action == 'ajouter':
            invités = input("Entrez les noms des invités à ajouter (séparés par une virgule): ").split(',')
            exposition.ajouter_invités([invité.strip() for invité in invités])
        elif action == 'enlever':
            invités = input("Entrez les noms des invités à enlever (séparés par une virgule): ").split(',')
            exposition.enlever_invités([invité.strip() for invité in invités])
        elif action == 'terminer':
            print("Gestion des invités terminée.")
            break
        else:
            print("Action non reconnue. Veuillez entrer 'ajouter', 'enlever', ou 'terminer'.")
     
        
def choisir_collections(collections):
    print("Collections disponibles:")
    for idx, collection in enumerate(collections, start=1):
        print(f"{idx}. {collection.nom}")

    choix = input("Entrez les numéros ou les noms des collections à inclure, séparés par des virgules: ")
    choix_split = choix.split(',')

    collections_exposees = []
    for item in choix_split:
        item = item.strip()
        if item.isdigit():
            index = int(item) - 1
            if 0 <= index < len(collections):
                collections_exposees.append(collections[index])
            else:
                print(f"Aucune collection trouvée à l'indice {item}")
        else:
            found = False
            for collection in collections:
                if collection.nom.lower() == item.lower():
                    collections_exposees.append(collection)
                    found = True
                    break
            if not found:
                print(f"Aucune collection trouvée avec le nom '{item}'")

    return collections_exposees



def main():
    fichier_donnees = "donnees.json"
    # Assurez-vous d'avoir quatre variables pour récupérer les données chargées
    artistes, oeuvres, collections, expositions = charger_donnees(fichier_donnees)

    while True:
        choix = input("Voulez-vous gérer un 'artiste', une 'oeuvre', une 'collection', 'exposition' ou 'quitter' ? ").strip().lower()
        if choix == 'quitter':
            break
        elif choix == 'artiste':
            creer_ou_trouver_artiste(artistes)
        elif choix == 'oeuvre':
            ajouter_ou_trouver_oeuvre(artistes, oeuvres)
        elif choix == 'collection':
            gerer_collection(artistes, oeuvres, collections)
        elif choix == 'exposition':
            gerer_expositions(collections, expositions)
        else:
            print("Choix non reconnu. Veuillez essayer à nouveau.")

    sauvegarder_donnees(fichier_donnees, artistes, oeuvres, collections, expositions)

if __name__ == "__main__":
    main()

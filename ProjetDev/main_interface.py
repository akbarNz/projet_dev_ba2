from Artiste import *
from Oeuvre import *
from Collection import *
from Exposition import *
import re
import json
from datetime import datetime

def demander_date_str(message, obligatoire=False):
    while True:
        date_str = input(message).strip()
        if not date_str and not obligatoire:
            return None
        if valider_format_date(date_str):
            return date_str
        print("Format de date invalide. Veuillez utiliser le format AAAA-MM-JJ (ex: 2024-12-16).")

def valider_format_date(date_str):
    if not date_str:
        return False

    match = re.match(r"(-?\d+)-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$", date_str)
    if not match:
        return False

    annee, mois, jour = match.groups()

    try:
        annee_positive = abs(int(annee))
        datetime(annee_positive, int(mois), int(jour))
        return True
    except ValueError:
        return False

def creer_ou_trouver_artiste(artistes):
    identite = input("Entrez le nom complet de l'artiste (Prénom Nom) : ").strip()
    artiste = trouver_artiste_par_nom(artistes, identite.lower())

    if artiste:
        print(f"Artiste trouvé : {artiste}")
        action = input("Voulez-vous 'voir' l'artiste ou 'modifier' ses informations ? (voir/modifier) : ").strip().lower()
        if action == 'voir':
            print(artiste)
        elif action == 'modifier':
            identite = input("Modifier nom et prénom (laisser vide pour ne pas modifier): ").strip()
            biographie = input("Nouvelle biographie (laisser vide pour ne pas modifier): ").strip()
            date_naissance = demander_date_str("Nouvelle date de naissance (AAAA-MM-JJ, laisser vide pour ne pas modifier): ")
            date_deces = demander_date_str("Nouvelle date de décès (AAAA-MM-JJ, laisser vide pour ne pas modifier): ")
            artiste.modifier(identite, biographie, date_naissance, date_deces)
            print(f"Artiste modifié : {artiste}")
    else:
        print("Artiste non trouvé.")
        if input("Voulez-vous créer cet artiste ? (oui/non) : ").strip().lower() == "oui":
            bio = input("Biographie : ").strip()
            date_naissance = demander_date_str("Date de naissance (AAAA-MM-JJ) : ", obligatoire=True)
            date_deces = demander_date_str("Date de décès (si applicable, sinon laisser vide) : ")
            new_artiste = Artiste(identite.title(), bio, date_naissance, date_deces)
            artistes.append(new_artiste)
            return new_artiste
    return None

def creer_ou_trouver_artiste2(artistes):
    identite = input("Entrez le nom complet de l'artiste (Prénom Nom) : ").strip()
    artiste = trouver_artiste_par_nom(artistes, identite.lower())

    if artiste:
        return artiste
    else:
        print("Artiste non trouvé.")
        if input("Voulez-vous créer cet artiste ? (oui/non) : ").strip().lower() == "oui":
            bio = input("Biographie : ").strip()
            date_naissance = demander_date_str("Date de naissance (AAAA-MM-JJ) : ")
            date_deces = demander_date_str("Date de décès (si applicable, sinon laisser vide) : ")
            new_artiste = Artiste(identite.title(), bio, date_naissance, date_deces)
            artistes.append(new_artiste)
            return new_artiste
    return None

def ajouter_oeuvres_multiples_a_collection(oeuvres, collection):
    print("Choisissez un critère pour ajouter des œuvres à la collection :")
    print("1. Artiste")
    print("2. Courant artistique")
    print("3. Couleur dominante")

    choix_utilisateur = input("Votre choix (ex: 1, 2, ou 3) : ").strip()

    if choix_utilisateur not in ['1', '2', '3']:
        print("Choix invalide. Veuillez choisir un critère valide.")
        return

    if choix_utilisateur == '1':
        critere = 'artiste'
        valeur_critere = input("Entrez le nom de l'artiste : ").strip().lower()
        oeuvres_filtrees = [o for o in oeuvres if o.artiste and o.artiste.identite.lower() == valeur_critere]
    elif choix_utilisateur == '2':
        critere = 'courant artistique'
        valeur_critere = input("Entrez le courant artistique : ").strip().lower()
        oeuvres_filtrees = [o for o in oeuvres if o.courant.lower() == valeur_critere]
    elif choix_utilisateur == '3':
        critere = 'couleur dominante'
        valeur_critere = input("Entrez la couleur dominante : ").strip().lower()
        oeuvres_filtrees = [o for o in oeuvres if o.couleur_dominante.lower() == valeur_critere]

    if not oeuvres_filtrees:
        print(f"Aucune œuvre ne correspond au critère '{critere}' avec la valeur '{valeur_critere}'.")
        return

    oeuvres_deja_presentes = [o for o in oeuvres_filtrees if o in collection.oeuvres]
    oeuvres_nouvelles = [o for o in oeuvres_filtrees if o not in collection.oeuvres]

    if oeuvres_deja_presentes:
        print(f"Les œuvres suivantes sont déjà présentes dans la collection '{collection.nom}':")
        for oeuvre in oeuvres_deja_presentes:
            print(f"- {oeuvre.titre}")

    if oeuvres_nouvelles:
        for oeuvre in oeuvres_nouvelles:
            collection.ajouter_oeuvre(oeuvre)
            print(f"'{oeuvre.titre}' a été ajoutée à la collection '{collection.nom}'.")
        #print(f"{len(oeuvres_nouvelles)} œuvre(s) ajoutée(s) à la collection.")
        print(f"{len(collection.oeuvres)} œuvre(s) ajoutée(s) à la collection.")
    else:
        if not oeuvres_deja_presentes:
            print("Aucune œuvre à ajouter selon les critères spécifiés.")

def ajouter_ou_trouver_oeuvre(artistes, oeuvres):
    titre = input("Entrez le titre de l'œuvre à rechercher ou créer: ").strip()
    oeuvre = trouver_oeuvre_par_titre(oeuvres, titre)

    if oeuvre:
        print(f"Œuvre trouvée : {oeuvre}")
        action = input("Que voulez-vous faire avec cette oeuvre ? (supprimer/ajouter(artiste si celui çi n'est pas encore lier)/Ne rien mettre si c'est pour ajouter à une collection) ")
        if action == 'supprimer':
            confirm = input(f"Êtes-vous sûr de vouloir supprimer l'œuvre '{oeuvre.titre}' ? (oui/non) : ").strip().lower()
            if confirm == 'oui':
                oeuvres.remove(oeuvre)
        if action == 'ajouter':           
            if oeuvre.artiste is None:
                if input("Cette œuvre n'a pas d'artiste assigné. Voulez-vous en ajouter un ? (oui/non) : ").strip().lower() == "oui":
                    artiste = creer_ou_trouver_artiste2(artistes)
                    if artiste:
                        oeuvre.assigner_artiste(artiste) 
                        print(f"L'artiste '{artiste.identite}' a été assigné à l'œuvre '{oeuvre.titre}'.")
            else:
                print("l'oeuvre à déjà un artiste")            
        return oeuvre

    if input("Œuvre non trouvée. Voulez-vous la créer ? (oui/non): ").strip().lower() == "oui":
        description = input("Description de l'œuvre: ").strip()
        apparition = input("l'année d'apparition de l'oeuvre : AAAA")
        couleur_dominante = input("Couleur dominante: ").strip()
        courant = input("Courant artistique: ").strip()
        choix_artiste = input("Artiste connu ? (oui/non): ")
        artiste = None
        if choix_artiste.lower() == 'oui':
            artiste = creer_ou_trouver_artiste2(artistes)
        oeuvre = Oeuvre(
            titre=titre,
            description=description,
            date_apparition=apparition,
            artiste=artiste,
            couleur_dominante=couleur_dominante,
            courant=courant
        )
        oeuvres.append(oeuvre)
        print(f"Nouvelle œuvre créée : {oeuvre}")
        return oeuvre
    return None

# NOUVEAU
def input_critere_tris():
    """demande les criteres de tri à l'utilisateur. Renvoie un tuple (date:bool, nom:bool)"""
    d = input("trier par la date d'apparition des oeuvres [y/n]: ")
    t = input("trier par le nom de l'oeuvre [y/n]: ")

    correct = False
    while not correct:
        if len(d) == 1 and len(t) == 1 and d.strip().lower() in 'ny' and t.strip().lower() in 'ny':
            correct = True
        else:
            print("valeur incorrect. veillez choisir entre [y/n]")
            d = input("trier par la date d'apparition des oeuvres [y/n]: ")
            t = input("trier par le nom de l'oeuvre [y/n]: ")

    if d == 'y' and t == 'y':
        return True, True
    elif d == 'n' and t == 'n':
        # tri par defaut est par date apparition
        return True, False
    elif d == 'y' and t == 'n':
        # tri par defaut est par date apparition
        return True, False
    elif t == 'y' and d == 'n':
        #tri par le nom de l'oeuvre
        return False, True


def gerer_collection(artistes, oeuvres, collections):
    choix_collection = input("Voulez-vous 'créer' une nouvelle collection ou 'modifier' une collection existante ? (créer/modifier) : ").strip().lower()
    collection = None
    try:
        if choix_collection in ['creer', 'créer']:
            nom_collection = input("Entrez le nom de la nouvelle collection : ").strip()
            collection = Collection(nom_collection)
            collections.append(collection)
            print(f"Nouvelle collection créée : {nom_collection}")
        elif choix_collection == 'modifier':
            collection = choisir_collection(collections) 
            if not collection:
                raise UnboundLocalError
            nom_collection = collection.nom
            print(f"Utilisation de la collection existante : {nom_collection}")
        else:
            print("Choix invalide.")
            return
    except UnboundLocalError:
        return

    while True:
        action = input("Voulez-vous ajouter 'une' oeuvre, 'plusieurs' oeuvres, 'trier' la collection 'supprimer' une oeuvre, ou 'supprimer' la collection ? (une/plusieurs/trier/supprimer/supprimer_collection) : ").strip().lower()
        if action == 'une':
            oeuvre = ajouter_ou_trouver_oeuvre(artistes, oeuvres)
            if oeuvre:
                collection.ajouter_oeuvre(oeuvre)
                print(f"L'oeuvre '{oeuvre.titre}' a été ajoutée à la collection '{nom_collection}'.")
        elif action == 'plusieurs':
            ajouter_oeuvres_multiples_a_collection(oeuvres, collection)
        # NOUVEAU
        elif action == 'trier':
            # verifie si collection vide
            if collection.est_vide():
                print("Collection vide. veillez rajouter des oeuvres avant de trier")
            else:
                # demander les criteres
                criteres = input_critere_tris()
                collection.tri_col(criteres[0], criteres[1])
                # affiche la collection trié
                print(collection)
        elif action == 'supprimer':
            oeuvre_a_supprimer = choisir_oeuvre_a_supprimer(collection)
            if oeuvre_a_supprimer:
                collection.enlever_oeuvre(oeuvre_a_supprimer)
                print(f"L'oeuvre '{oeuvre_a_supprimer.titre}' a été supprimée de la collection '{nom_collection}'.")
        elif action == 'supprimer_collection':
            confirmation = input(f"Êtes-vous sûr de vouloir supprimer la collection '{nom_collection}' ? (oui/non) : ").strip().lower()
            if confirmation == 'oui':
                collections.remove(collection)
                print(f"La collection '{nom_collection}' a été supprimée.")
                return 
        else:
            print("Choix invalide. Veuillez choisir 'une', 'plusieurs', 'supprimer' ou 'supprimer_collection'.")
            continue
        
        encore = input("Voulez-vous effectuer d'autres actions sur cette collection ? (oui/non) : ").strip().lower()
        if encore != 'oui':
            break

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
        return collections[int(choix) - 1]
    except (ValueError, IndexError):
        return next((col for col in collections if col.nom.lower() == choix), None)

def choisir_oeuvre_a_supprimer(collection):
    if not collection.oeuvres:
        print("Aucune œuvre dans cette collection.")
        return None
    print("Œuvres dans la collection :")
    for idx, oeuvre in enumerate(collection.oeuvres, start=1):
        print(f"{idx}. {oeuvre.titre}")
    choix = input("Choisissez une œuvre à supprimer par numéro ou entrez le titre : ").strip().lower()
    try:
        return collection.oeuvres[int(choix) - 1]
    except (ValueError, IndexError):
        return next((oeuvre for oeuvre in collection.oeuvres if oeuvre.titre.lower() == choix), None)


def gerer_expositions(collections, expositions):
    choix = input("Voulez-vous 'creer' une nouvelle exposition, 'modifier' une exposition existante, ou 'voir' les expositions existantes ? (creer/modifier/voir) : ").strip().lower()
    if choix == 'creer':
        date = demander_date_str("Entrez la date de l'exposition (AAAA-MM-JJ): ", obligatoire=True)
        collections_exposees = choisir_collections(collections)
        exposition = Exposition(collections_exposees, date)
        gerer_invites(exposition)
        expositions.append(exposition)
        print(f"Exposition prevue le {date} creee.")
    elif choix == 'modifier':
        date = demander_date_str("Entrez la date de l'exposition a modifier (AAAA-MM-JJ): ", obligatoire=True)
        exposition = next((expo for expo in expositions if expo.date == date), None)
        if exposition:
            while True:
                action = input("Voulez-vous 'ajouter' des invites, 'enlever' des invites, 'supprimer' l'exposition, 'enlever collections', ou 'terminer' ? (ajouter/enlever/supprimer/enlever collections/terminer) : ").strip().lower()
                if action == 'ajouter':
                    invites = input("Entrez les noms des invites a ajouter (separes par une virgule): ").split(',')
                    exposition.ajouter_invites([invite.strip() for invite in invites])
                    print(f"{len(invites)} invites ajoutes.")
                elif action == 'enlever':
                    invites = input("Entrez les noms des invites a enlever (separes par une virgule): ").split(',')
                    exposition.enlever_invites([invite.strip() for invite in invites])
                    print(f"{len(invites)} invites enleves.")
                elif action == 'supprimer':
                    expositions.remove(exposition)
                    print(f"L'exposition prevue le {date} a ete supprimee.")
                    break
                elif action == 'enlever collections':
                    nom_collection = input("Entrez le nom de la collection a enlever : ").strip()
                    collection = next((col for col in exposition.collections if col.nom == nom_collection), None)
                    if collection:
                        exposition.supprimer_collection(collection)
                        print(f"La collection '{nom_collection}' a ete enlevee de l'exposition.")
                    else:
                        print(f"La collection '{nom_collection}' n'est pas presente dans cette exposition.")
                elif action == 'terminer':
                    print("Modification terminee.")
                    break
                else:
                    print("Action non reconnue. Veuillez reessayer.")
        else:
            print("Aucune exposition trouvee pour cette date.")
    elif choix == 'voir':
        if expositions:
            for expo in expositions:
                print(expo)
        else:
            print("Aucune exposition existante.")
    else:
        print("Choix invalide.")

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
                print(f"Aucune collection trouvee a l'indice {item}")
        else:
            found = False
            for collection in collections:
                if collection.nom.lower() == item.lower():
                    collections_exposees.append(collection)
                    found = True
                    break
            if not found:
                print(f"Aucune collection trouvee avec le nom '{item}'")

    return collections_exposees

def gerer_invites(exposition):
    while True:
        action = input("Voulez-vous 'ajouter' des invites, 'enlever' des invites, ou 'terminer' ? (ajouter/enlever/terminer) ").strip().lower()
        if action == 'ajouter':
            invites = input("Entrez les noms des invites a ajouter (separes par une virgule): ").split(',')
            exposition.ajouter_invites([invite.strip() for invite in invites])
            print(f"{len(invites)} invites ajoutes.")
        elif action == 'enlever':
            invites = input("Entrez les noms des invites a enlever (separes par une virgule): ").split(',')
            exposition.enlever_invites([invite.strip() for invite in invites])
            print(f"{len(invites)} invites enleves.")
        elif action == 'terminer':
            print("Gestion des invites terminee.")
            break
        else:
            print("Action non reconnue. Veuillez entrer 'ajouter', 'enlever', ou 'terminer'.")

def sauvegarder_donnees(fichier, artistes, oeuvres, collections, expositions):
    # ajout de tri avant la sauvegarde par exemple
    data = {
        "artistes": [artiste.to_dict() for artiste in artistes],
        "oeuvres": [oeuvre.to_dict() for oeuvre in oeuvres],
        "collections": [collection.to_dict() for collection in collections],
        "expositions": [exposition.to_dict() for exposition in expositions]
    }
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Données sauvegardées avec succès.")
    
def charger_donnees(fichier):
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            data = json.load(f)
            artistes = [Artiste.from_dict(a) for a in data.get("artistes", [])]
            oeuvres = [Oeuvre.from_dict(o, artistes) for o in data.get("oeuvres", [])]
            collections = [Collection.from_dict(c, oeuvres) for c in data.get("collections", [])]
            expositions = [Exposition.from_dict(e, collections) for e in data.get("expositions", [])]
            return artistes, oeuvres, collections, expositions
    except FileNotFoundError:
        print("Fichier de données non trouvé.")
        return [], [], [], []
    except json.JSONDecodeError as e:
        print(f"Erreur de lecture JSON : {e}")
        return [], [], [], []

def main():
    fichier_donnees = "donnees.json"
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

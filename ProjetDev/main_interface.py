from Artiste import *
from Oeuvre import *
from Collection import *
from Exposition import *

def demander_date_str(message, obligatoire=False):
    while True:
        date_str = input(message).strip()
        if not date_str and not obligatoire:
            return None
        if valider_format_date(date_str):
            return date_str
        print("Format de date invalide. Veuillez utiliser le format AAAA-MM-JJ.")


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
            date_naissance = input("Nouvelle date de naissance (AAAA-MM-JJ, laisser vide pour ne pas modifier): ").strip()
            date_deces = input("Nouvelle date de décès (AAAA-MM-JJ, laisser vide pour ne pas modifier): ").strip()
            artiste.modifier(biographie, date_naissance, date_deces)
            print(f"Artiste modifié : {artiste}")
    else:
        print("Artiste non trouvé.")
        if input("Voulez-vous créer cet artiste ? (oui/non) : ").strip().lower() == "oui":
            bio = input("Biographie : ").strip()
            date_naissance = input("Date de naissance (AAAA-MM-JJ) : ").strip()
            date_deces = input("Date de décès (si applicable, sinon laisser vide) : ").strip() or None
            new_artiste = Artiste(identite.title(), bio, date_naissance, date_deces)
            artistes.append(new_artiste)
            return new_artiste
    return None

def creer_ou_trouver_artiste2(artistes):
    identite = input("Entrez le nom complet de l'artiste (Prénom Nom) : ").strip()
    artiste = trouver_artiste_par_nom(artistes, identite.lower())

    if artiste:
        print(f"Artiste trouvé : {artiste}")
    else:
        print("Artiste non trouvé.")
        if input("Voulez-vous créer cet artiste ? (oui/non) : ").strip().lower() == "oui":
            bio = input("Biographie : ").strip()
            date_naissance = input("Date de naissance (AAAA-MM-JJ) : ").strip()
            date_deces = input("Date de décès (si applicable, sinon laisser vide) : ").strip() or None
            new_artiste = Artiste(identite.title(), bio, date_naissance, date_deces)
            artistes.append(new_artiste)
            return new_artiste
    return None


def ajouter_oeuvres_multiples_a_collection(oeuvres, collection):
    print("Choisissez un ou plusieurs critères pour ajouter des œuvres à la collection (séparez par des virgules) :")
    print("1. Artiste")
    print("2. Courant artistique")
    print("3. Couleur dominante")
    choix_utilisateur = input("Votre choix (ex: 1, 2, 3) : ").strip()

    oeuvres_a_ajouter = []
    critere = None

    choixs = choix_utilisateur.split(',')
    for choix in choixs:
        choix = choix.strip()
        if choix == '1' or choix.lower() == 'artiste':
            critere = input("Entrez le nom de l'artiste : ").strip().lower()
            oeuvres_a_ajouter.extend([o for o in oeuvres if o.artiste and o.artiste.identite.lower() == critere])
        elif choix == '2' or choix.lower() == 'courant artistique':
            critere = input("Entrez le courant artistique : ").strip().lower()
            oeuvres_a_ajouter.extend([o for o in oeuvres if o.courant.lower() == critere])
        elif choix == '3' or choix.lower() == 'couleur dominante':
            critere = input("Entrez la couleur dominante : ").strip().lower()
            oeuvres_a_ajouter.extend([o for o in oeuvres if o.couleur_dominante.lower() == critere])
        else:
            print("Choix invalide.")
            return

    oeuvres_a_ajouter = list(set(oeuvres_a_ajouter))

    oeuvres_deja_presentes = [o for o in oeuvres_a_ajouter if o in collection.oeuvres]
    oeuvres_nouvelles = [o for o in oeuvres_a_ajouter if o not in collection.oeuvres]

    if oeuvres_deja_presentes:
        print(f"Les œuvres suivantes sont déjà présentes dans la collection '{collection.nom}':")
        for oeuvre in oeuvres_deja_presentes:
            print(f"- {oeuvre.titre}")

    if oeuvres_nouvelles:
        for oeuvre in oeuvres_nouvelles:
            collection.ajouter_oeuvre(oeuvre)
            print(f"'{oeuvre.titre}' a été ajoutée à la collection '{collection.nom}'.")
        print(f"{len(oeuvres_nouvelles)} œuvre(s) ajoutée(s) à la collection.")
    else:
        if not oeuvres_deja_presentes:
            print("Aucune nouvelle œuvre à ajouter selon les critères spécifiés.")


def ajouter_ou_trouver_oeuvre(artistes, oeuvres):
    titre = input("Entrez le titre de l'œuvre à rechercher ou créer: ").strip()
    oeuvre = trouver_oeuvre_par_titre(oeuvres, titre)
    if oeuvre:
        print(f"Œuvre trouvée : {oeuvre}")
        if oeuvre.artiste is None:
            if input("Cette œuvre n'a pas d'artiste assigné. Voulez-vous en ajouter un ? (oui/non) : ").strip().lower() == "oui":
                artiste = creer_ou_trouver_artiste2(artistes)
                if artiste:
                    oeuvre.assigner_artiste(artiste)  # S'assurer que cette méthode est bien définie dans la classe Oeuvre.
                    print(f"L'artiste '{artiste.identite}' a été assigné à l'œuvre '{oeuvre.titre}'.")
        return oeuvre

    if input("Œuvre non trouvée. Voulez-vous la créer ? (oui/non): ").strip().lower() == "oui":
        description = input("Description de l'œuvre: ").strip()
        couleur_dominante = input("Couleur dominante: ").strip()
        courant = input("Courant artistique: ").strip()
        choix_artiste = input("Artiste connu ? (oui/non): ")
        artiste = None
        if choix_artiste.lower() == 'oui':
            artiste = creer_ou_trouver_artiste2(artistes)
        oeuvre = Oeuvre(
            titre=titre,
            description=description,
            artiste=artiste,
            couleur_dominante=couleur_dominante,
            courant=courant
        )
        oeuvres.append(oeuvre)
        print(f"Nouvelle œuvre créée : {oeuvre}")
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
        return collections[int(choix) - 1]
    except (ValueError, IndexError):
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
        nom_collection = collection.nom
        print(f"Utilisation de la collection existante : {nom_collection}")
    else:
        print("Choix invalide.")
        return

    while True:
        action = input("Voulez-vous 'ajouter', 'retirer' une oeuvre ou 'terminer' ? (ajouter/retirer/terminer) : ").strip().lower()
        if action == 'ajouter':
            oeuvre = ajouter_ou_trouver_oeuvre(artistes, oeuvres)
            if oeuvre:
                collection.ajouter_oeuvre(oeuvre)
                print(f"L'œuvre '{oeuvre.titre}' a été ajoutée à la collection '{nom_collection}'.")
        elif action == 'retirer':
            titre = input("Entrez le titre de l'œuvre à retirer : ").strip()
            oeuvre = trouver_oeuvre_par_titre(oeuvres, titre)
            if oeuvre:
                collection.enlever_oeuvre(oeuvre)
        elif action == 'terminer':
            break
        else:
            print("Choix invalide.")

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
        date = input("Entrez la date de l'exposition à modifier (AAAA-MM-JJ): ").strip()
        exposition = next((expo for expo in expositions if expo.date == date), None)
        if exposition:
            while True:
                action = input("Voulez-vous 'ajouter' des invités, 'enlever' des invités, 'supprimer' l'exposition, 'enlever collections', ou 'terminer' ? (ajouter/enlever/supprimer/enlever collections/terminer) : ").strip().lower()
                if action == 'ajouter':
                    invités = input("Entrez les noms des invités à ajouter (séparés par une virgule): ").split(',')
                    exposition.ajouter_invités([invité.strip() for invité in invités])
                elif action == 'enlever':
                    invités = input("Entrez les noms des invités à enlever (séparés par une virgule): ").split(',')
                    exposition.enlever_invités([invité.strip() for invité in invités])
                elif action == 'supprimer':
                    expositions.remove(exposition)
                    print(f"L'exposition prévue le {date} a été supprimée.")
                    break
                elif action == 'enlever collections':
                    nom_collection = input("Entrez le nom de la collection à enlever : ").strip()
                    collection = next((col for col in exposition.collections if col.nom == nom_collection), None)
                    if collection:
                        exposition.supprimer_collection(collection)
                    else:
                        print(f"La collection '{nom_collection}' n'est pas présente dans cette exposition.")
                elif action == 'terminer':
                    print("Modification terminée.")
                    break
                else:
                    print("Action non reconnue. Veuillez réessayer.")
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

def supprimer_oeuvre(oeuvres, collections):
    titre = input("Entrez le titre de l'\u0153uvre à supprimer : ").strip()
    oeuvre = trouver_oeuvre_par_titre(oeuvres, titre)
    if oeuvre:
        for collection in collections:
            collection.supprimer_oeuvre(oeuvre)
        oeuvres.remove(oeuvre)
        print(f"L'\u0153uvre '{titre}' a été supprimée de toutes les collections et du système.")
    else:
        print(f"L'\u0153uvre '{titre}' n'a pas été trouvée.")

def supprimer_collection(collections, expositions):
    nom = input("Entrez le nom de la collection à supprimer : ").strip()
    collection = next((c for c in collections if c.nom == nom), None)
    if collection:
        for exposition in expositions:
            exposition.supprimer_collection(collection)
        collections.remove(collection)
        print(f"La collection '{nom}' a été supprimée de toutes les expositions et du système.")
    else:
        print(f"La collection '{nom}' n'a pas été trouvée.")

def supprimer_exposition(expositions):
    date = input("Entrez la date de l'exposition à supprimer (AAAA-MM-JJ) : ").strip()
    exposition = next((e for e in expositions if e.date == date), None)
    if exposition:
        expositions.remove(exposition)
        print(f"L'exposition prévue le {date} a été supprimée.")
    else:
        print(f"Aucune exposition trouvée pour la date {date}.")



def supprimer_oeuvre(oeuvres, collections):
    titre = input("Entrez le titre de l'\u0153uvre à supprimer : ").strip()
    oeuvre = trouver_oeuvre_par_titre(oeuvres, titre)
    if oeuvre:
        for collection in collections:
            collection.supprimer_oeuvre(oeuvre)
        oeuvres.remove(oeuvre)
        print(f"L'\u0153uvre '{titre}' a été supprimée de toutes les collections et du système.")
    else:
        print(f"L'\u0153uvre '{titre}' n'a pas été trouvée.")

def supprimer_collection(collections, expositions):
    nom = input("Entrez le nom de la collection à supprimer : ").strip()
    collection = next((c for c in collections if c.nom == nom), None)
    if collection:
        for exposition in expositions:
            exposition.supprimer_collection(collection)
        collections.remove(collection)
        print(f"La collection '{nom}' a été supprimée de toutes les expositions et du système.")
    else:
        print(f"La collection '{nom}' n'a pas été trouvée.")

def supprimer_exposition(expositions):
    date = input("Entrez la date de l'exposition à supprimer (AAAA-MM-JJ) : ").strip()
    exposition = next((e for e in expositions if e.date == date), None)
    if exposition:
        expositions.remove(exposition)
        print(f"L'exposition prévue le {date} a été supprimée.")
    else:
        print(f"Aucune exposition trouvée pour la date {date}.")


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

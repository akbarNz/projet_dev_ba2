import unittest
import Artiste
import Oeuvre
import Exposition
import Collection
from main_interface import *
from datetime import date


class TestClassesArt(unittest.TestCase):

    def setUp(self):
        # Création des artistes
        self.artiste1 = Artiste("Vincent Van Gogh", "Peintre néerlandais", "1853-03-30", "1890-07-29")
        self.artiste2 = Artiste("Pablo Picasso", "Peintre espagnol", "1881-10-25", "1973-04-08")

        # Création des oeuvres
        self.oeuvre1 = Oeuvre("La Nuit étoilée", "Une peinture célèbre de Van Gogh", self.artiste1, "Bleu",
                              "Post-Impressionnisme")
        self.oeuvre2 = Oeuvre("Les Demoiselles d'Avignon", "Une peinture majeure de Picasso", self.artiste2, "Rose",
                              "Cubisme")

        # Création des collections
        self.collection1 = Collection("Impressionnisme")
        self.collection1.ajouter_oeuvre(self.oeuvre1)
        self.collection2 = Collection("Cubisme")
        self.collection2.ajouter_oeuvre(self.oeuvre2)

        # Création d'une exposition
        self.exposition = Exposition([self.collection1, self.collection2], "2024-01-01",
                                     ["Critique d'art", "Historien"])

    def test_artiste(self):
        self.assertEqual(self.artiste1.identite, "Vincent Van Gogh")
        self.assertEqual(self.artiste2.date_deces, "1973-04-08")

        self.artiste1.modifier(biographie="Un des peintres les plus célèbres au monde")
        self.assertEqual(self.artiste1.biographie, "Un des peintres les plus célèbres au monde")

    def test_oeuvre(self):
        self.assertEqual(self.oeuvre1.titre, "La Nuit étoilée")
        self.assertEqual(self.oeuvre1.artiste.identite, "Vincent Van Gogh")

        # Test d'assignation multiple sans exception
        self.oeuvre1.assigner_artiste(self.artiste1)  # Pas d'effet attendu

    def test_collection(self):
        self.assertEqual(self.collection1.nom, "Impressionnisme")
        self.assertIn(self.oeuvre1, self.collection1.oeuvres)

        self.collection1.enlever_oeuvre(self.oeuvre1)
        self.assertNotIn(self.oeuvre1, self.collection1.oeuvres)

        # Test suppression d'une œuvre inexistante
        self.collection1.enlever_oeuvre(self.oeuvre2)  # Ne doit pas lever d'exception

        # Test ajout d'œuvre en double
        self.collection1.ajouter_oeuvre(self.oeuvre1)
        self.collection1.ajouter_oeuvre(self.oeuvre1)  # Pas d'effet attendu
        self.assertEqual(len(self.collection1.oeuvres), 1)

    def test_exposition(self):
        self.assertEqual(len(self.exposition.collections), 2)
        self.assertIn("Critique d'art", self.exposition.invites)

        self.exposition.ajouter_invites(["Photographe"])
        self.assertIn("Photographe", self.exposition.invites)

        self.exposition.enlever_invites(["Critique d'art"])
        self.assertNotIn("Critique d'art", self.exposition.invites)

        self.exposition.supprimer_toutes_les_collections()
        self.assertEqual(len(self.exposition.collections), 0)

    def test_exceptions(self):

        # Création d'une collection avec un attribut manquant
        with self.assertRaises(TypeError):
            Collection()  # Nom obligatoire

    def test_trouver_artiste_par_nom(self):
        artistes = [self.artiste1, self.artiste2]
        artiste = trouver_artiste_par_nom(artistes, "Pablo Picasso")
        self.assertEqual(artiste, self.artiste2)

        artiste = trouver_artiste_par_nom(artistes, "Claude Monet")
        self.assertIsNone(artiste)

    def test_trouver_oeuvre_par_titre(self):
        oeuvres = [self.oeuvre1, self.oeuvre2]
        oeuvre = trouver_oeuvre_par_titre(oeuvres, "La Nuit étoilée")
        self.assertEqual(oeuvre, self.oeuvre1)

        oeuvre = trouver_oeuvre_par_titre(oeuvres, "Le Cri")
        self.assertIsNone(oeuvre)

    def test_assigner_artiste(self):
        # Cas 1 : Assigner un artiste si aucun artiste n'est assigné
        oeuvre_sans_artiste = Oeuvre("Sans titre", "Description", None, "Rouge", "Abstrait")
        self.assertIsNone(oeuvre_sans_artiste.artiste)  # Vérifier qu'il n'y a pas d'artiste assigné

        oeuvre_sans_artiste.assigner_artiste(self.artiste1)  # Assigner un artiste
        self.assertEqual(oeuvre_sans_artiste.artiste, self.artiste1)  # Vérifier l'assignation

        # Cas 2 : Ne pas remplacer un artiste déjà assigné
        oeuvre_sans_artiste.assigner_artiste(self.artiste2)  # Tenter de remplacer l'artiste
        self.assertEqual(oeuvre_sans_artiste.artiste, self.artiste1)  # Vérifier que l'artiste reste inchangé

    def test_oeuvre_str(self):
        # Cas 1 : Œuvre avec un artiste assigné
        expected_str = (
            "Oeuvre: La Nuit étoilée, Artiste: Vincent Van Gogh, Description: Une peinture célèbre de Van Gogh, "
            "Couleur Dominante: Bleu, Courant: Post-Impressionnisme")
        self.assertEqual(str(self.oeuvre1), expected_str)

        # Cas 2 : Œuvre sans artiste assigné
        oeuvre_sans_artiste = Oeuvre("Sans titre", "Description inconnue", None, "Gris", "Minimalisme")
        expected_str_sans_artiste = ("Oeuvre: Sans titre, Artiste: Inconnu, Description: Description inconnue, "
                                     "Couleur Dominante: Gris, Courant: Minimalisme")
        self.assertEqual(str(oeuvre_sans_artiste), expected_str_sans_artiste)

    def test_exposition_str(self):
        # Cas 1 : Exposition avec des collections et des invités
        expected_str = ("Exposition le 2024-01-01, Collections: ['Impressionnisme', 'Cubisme'], "
                        "Invites: Critique d'art, Historien")
        self.assertEqual(str(self.exposition), expected_str)

        # Cas 2 : Exposition sans invités
        exposition_sans_invites = Exposition([self.collection1], "2025-05-15", [])
        expected_str_sans_invites = "Exposition le 2025-05-15, Collections: ['Impressionnisme'], Invites: Aucun"
        self.assertEqual(str(exposition_sans_invites), expected_str_sans_invites)

        # Cas 3 : Exposition sans collections ni invités
        exposition_vide = Exposition([], "2026-12-31", [])
        expected_str_vide = "Exposition le 2026-12-31, Collections: [], Invites: Aucun"
        self.assertEqual(str(exposition_vide), expected_str_vide)

    def test_supprimer_collection(self):
        # Vérifie qu'une collection est supprimée correctement
        self.exposition.supprimer_collection(self.collection1)
        self.assertNotIn(self.collection1, self.exposition.collections)
        self.assertIn(self.collection2, self.exposition.collections)

        # Vérifie que supprimer une collection absente ne provoque pas d'erreur
        collection_inexistante = Collection("Suréalisme")
        self.exposition.supprimer_collection(collection_inexistante)  # Pas d'erreur attendue
        self.assertEqual(len(self.exposition.collections), 1)  # Toujours une collection restante

    def test_to_dict(self):
        # Appel de la méthode to_dict
        expo_dict = self.exposition.to_dict()

        # Vérifie le contenu du dictionnaire
        self.assertEqual(expo_dict["collections"], ["Impressionnisme", "Cubisme"])
        self.assertEqual(expo_dict["date"], "2024-01-01")
        self.assertEqual(expo_dict["invites"], ["Critique d'art", "Historien"])

        # Vérifie le comportement avec une exposition vide
        exposition_vide = Exposition([], "2026-12-31", [])
        expo_dict_vide = exposition_vide.to_dict()
        self.assertEqual(expo_dict_vide["collections"], [])
        self.assertEqual(expo_dict_vide["date"], "2026-12-31")
        self.assertEqual(expo_dict_vide["invites"], [])

    def test_collection_str(self):
        # Tester la représentation en chaîne de la collection
        self.collection1.ajouter_oeuvre(self.oeuvre1)
        self.collection1.ajouter_oeuvre(self.oeuvre2)

        # Vérification de la sortie de la méthode __str__
        str_collection = str(self.collection1)
        self.assertIn("Impressionnisme", str_collection)  # Le nom de la collection doit être présent
        self.assertIn(self.oeuvre1.titre, str_collection)  # Le titre de l'œuvre1 doit être présent
        self.assertIn(self.oeuvre2.titre, str_collection)  # Le titre de l'œuvre2 doit être présent

    def test_artiste_str(self):
        # Tester la représentation en chaîne de l'artiste
        artiste_str = str(self.artiste1)
        self.assertIn(self.artiste1.identite, artiste_str)  # L'identité de l'artiste doit être présente
        self.assertIn(self.artiste1.biographie, artiste_str)  # La biographie de l'artiste doit être présente
        self.assertIn(self.artiste1.date_naissance, artiste_str)  # La date de naissance doit être présente

    def test_artiste_to_dict(self):
        # Tester la conversion de l'artiste en dictionnaire
        artiste_dict = self.artiste1.to_dict()

        # Vérification de la présence des informations attendues
        self.assertEqual(artiste_dict["identite"], self.artiste1.identite)
        self.assertEqual(artiste_dict["biographie"], self.artiste1.biographie)
        self.assertEqual(artiste_dict["date_naissance"], self.artiste1.date_naissance)
        self.assertEqual(artiste_dict["date_deces"], self.artiste1.date_deces)

    def test_nom_setter(self):
        # Test si le setter change bien le nom
        self.collection1.nom = "Nouveau Nom"
        self.assertEqual(self.collection1.nom, "Nouveau Nom")

    def test_from_dict(self):
        data = {
            "identite": "Vincent Van Gogh",
            "biographie": "Peintre néerlandais, célèbre pour ses tableaux.",
            "date_naissance": "1853-03-30",
            "date_deces": "1890-07-29"
        }
        artiste = Artiste.from_dict(data)

        # Vérifie que l'Artiste a bien été créé à partir du dictionnaire
        self.assertEqual(artiste.identite, "Vincent Van Gogh")
        self.assertEqual(artiste.biographie, "Peintre néerlandais, célèbre pour ses tableaux.")
        self.assertEqual(artiste.date_naissance, "1853-03-30")
        self.assertEqual(artiste.date_deces, "1890-07-29")

    def test_modifier(self):
        # Création d'un artiste
        artiste = Artiste("Claude Monet", "Peintre français", "1840-11-14")

        # Modification de l'artiste
        artiste.modifier(identite="Claude Monet (Modifié)",
                         biographie="Peintre français, chef de file de l'impressionnisme", date_deces="1926-12-05")

        # Vérification des modifications
        self.assertEqual(artiste.identite, "Claude Monet (Modifié)")
        self.assertEqual(artiste.biographie, "Peintre français, chef de file de l'impressionnisme")
        self.assertEqual(artiste.date_deces, "1926-12-05")

    def test_to_dict_and_from_dict(self):
        oeuvre_dict = self.oeuvre1.to_dict()
        self.assertEqual(oeuvre_dict["titre"], "La Nuit étoilée")

        oeuvre_from_dict = Oeuvre.from_dict(oeuvre_dict, [self.artiste1, self.artiste2])
        self.assertEqual(oeuvre_from_dict.titre, self.oeuvre1.titre)

        collection_dict = self.collection1.to_dict()
        self.assertIn("La Nuit étoilée", collection_dict["oeuvres"])

        collection_from_dict = Collection.from_dict(collection_dict, [self.oeuvre1, self.oeuvre2])
        self.assertEqual(collection_from_dict.nom, self.collection1.nom)

if __name__ == "__main__":
    unittest.main()

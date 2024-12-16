import unittest
# Importation des classes nécessaires depuis vos modules
from Artiste import Artiste
from Oeuvre import Oeuvre
from Collection import Collection
from Exposition import Exposition

# Définition de la classe de test, qui hérite de unittest.TestCase pour accéder à ses fonctionnalités de test
class TestGalerieArt(unittest.TestCase):
    def setUp(self):
        
        # Méthode setUp qui configure l'environnement de test avant chaque méthode de test
        # Création des instances d'artistes avec des informations détaillées
        
        self.artiste1 = Artiste("Vincent van Gogh", "Peintre postimpressionniste néerlandais.", "1853-03-30", "1890-07-29")
        self.artiste2 = Artiste("Claude Monet", "Fondateur de l'impressionnisme français.", "1840-11-14", "1926-12-05")
        
        
        # Création des œuvres en associant les artistes précédemment créés
        
        self.oeuvre1 = Oeuvre("Nuit étoilée", "Une des oeuvres les plus reconnues de Van Gogh.", self.artiste1, "Bleu", "Post-impressionnisme")
        self.oeuvre2 = Oeuvre("Impression, soleil levant", "C'est cette peinture qui a donné son nom à l'impressionnisme.", self.artiste2, "Orange", "Impressionnisme")
        
        
        # Création d'une collection et ajout d'une œuvre à cette collection
        
        self.collection = Collection("Impressionnisme")
        self.collection.ajouter_oeuvre(self.oeuvre1)
        
        
        # Création d'une exposition qui inclut la collection
        
        self.exposition = Exposition([self.collection], "2021-10-01")


    # Test pour vérifier que l'artiste est correctement initialisé avec ses attributs
    
    def test_artiste_creation(self):
        self.assertEqual(self.artiste1.identite, "Vincent van Gogh")
        self.assertEqual(self.artiste1.biographie, "Peintre postimpressionniste néerlandais.")


    # Test pour vérifier que l'artiste est bien assigné à l'œuvre lors de la création de l'œuvre
    
    def test_oeuvre_affectation_artiste(self):
        self.assertEqual(self.oeuvre1.artiste, self.artiste1)


    # Test pour vérifier que l'œuvre est correctement ajoutée à la collection
    
    def test_collection_ajout_oeuvre(self):
        self.assertIn(self.oeuvre1, self.collection.oeuvres)


    # Test pour vérifier l'ajout d'invités à une exposition
    
    def test_exposition_ajout_invites(self):
        self.exposition.ajouter_invites(["Elton John"])
        self.assertIn("Elton John", self.exposition.invites)


    # Test pour vérifier la suppression d'invités d'une exposition
    
    def test_exposition_retirer_invites(self):
        self.exposition.enlever_invites(["Bob Dylan"])
        self.assertNotIn("Bob Dylan", self.exposition.invites)

    # Test pour vérifier que la description de l'œuvre est bien formée et contient les informations attendues
    def test_oeuvre_description(self):
        description = str(self.oeuvre1)
        self.assertIn("Une des oeuvres les plus reconnues de Van Gogh.", description)
    
    # Test pour s'assurer qu'une œuvre peut être ajoutée à une collection et qu'elle y figure bien
    def test_ajout_oeuvre_collection(self):
        self.collection.ajouter_oeuvre(self.oeuvre1)
        self.assertIn(self.oeuvre1, self.collection.oeuvres)

    # Test pour vérifier que l'exposition est correctement initialisée avec les collections et la date spécifiée
    def test_initialisation_exposition(self):
        self.assertIn(self.collection, self.exposition.collections)
        self.assertEqual(self.exposition.date, "2021-10-01")

if __name__ == '__main__':
    unittest.main()  

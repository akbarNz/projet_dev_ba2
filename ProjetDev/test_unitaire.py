import unittest
from Artiste import Artiste
from Oeuvre import Oeuvre
from Collection import Collection
from Exposition import Exposition

class TestGalerieArt(unittest.TestCase):
    def setUp(self):
        """Setup test fixtures."""
        self.artiste1 = Artiste("Vincent van Gogh", "Peintre postimpressionniste néerlandais.", "1853-03-30", "1890-07-29")
        self.artiste2 = Artiste("Claude Monet", "Fondateur de l'impressionnisme français.", "1840-11-14", "1926-12-05")
        self.oeuvre1 = Oeuvre("Nuit étoilée", "Une des œuvres les plus reconnues de Van Gogh.", self.artiste1, "Bleu", "Post-impressionnisme")
        self.oeuvre2 = Oeuvre("Impression, soleil levant", "C'est cette peinture qui a donné son nom à l'impressionnisme.", self.artiste2, "Orange", "Impressionnisme")
        self.collection = Collection("Impressionnisme")
        self.collection.ajouter_oeuvre(self.oeuvre2)
        self.exposition = Exposition([self.collection], "2021-10-01", ["Alice Merton", "Bob Dylan"])

    def test_modification_artiste(self):
        """Test artist's information modification."""
        self.artiste1.modifier("Un peintre célèbre", "1853-03-30", "1890-07-29")
        self.assertEqual(self.artiste1.biographie, "Un peintre célèbre")

    def test_ajout_oeuvre_inexistante(self):
        """Test adding a non-existent artwork to the collection and ensure it is added."""
        self.collection.ajouter_oeuvre(self.oeuvre1)
        self.assertIn(self.oeuvre1, self.collection.oeuvres)

    def test_ajout_oeuvre_existante(self):
        """Test adding an existing artwork to the collection and ensure it is not duplicated."""
        self.collection.ajouter_oeuvre(self.oeuvre2)
        self.assertEqual(self.collection.oeuvres.count(self.oeuvre2), 1)

    def test_creation_exposition(self):
        """Test creating an exhibition with given collections and guests."""
        self.assertIn(self.collection, self.exposition.collections)
        self.assertIn("Bob Dylan", self.exposition.invités)

    def test_ajouter_invites_exposition(self):
        """Test adding guests to the exhibition."""
        self.exposition.ajouter_invités(["Elton John"])
        self.assertIn("Elton John", self.exposition.invités)

    def test_enlever_invites_exposition(self):
        """Test removing guests from the exhibition."""
        self.exposition.enlever_invités(["Alice Merton"])
        self.assertNotIn("Alice Merton", self.exposition.invités)

    def test_recherche_oeuvre_par_titre(self):
        """Test searching for an artwork by title within the collection."""
        found = self.collection.trouver_oeuvre_par_titre("Impression, soleil levant")
        self.assertEqual(found, self.oeuvre2)

    def test_validation_date_creation_oeuvre(self):
        """Test the date validation when creating an artwork."""
        with self.assertRaises(ValueError):
            Oeuvre("Test", "Test description", self.artiste1, "Bleu", "Test", date_creation="wrong-date")

    def test_ajout_multiple_oeuvres(self):
        """Test adding multiple artworks to a collection."""
        new_oeuvre = Oeuvre("Le Déjeuner sur l'herbe", "Un célèbre tableau de Manet.", self.artiste2, "Vert", "Impressionnisme")
        self.collection.ajouter_oeuvres([self.oeuvre1, new_oeuvre])
        self.assertIn(new_oeuvre, self.collection.oeuvres)
        self.assertIn(self.oeuvre1, self.collection.oeuvres)

    def test_modification_exposition(self):
        """Test modifications to an exhibition's details."""
        self.exposition.modifier_date("2022-01-01")
        self.assertEqual(self.exposition.date, "2022-01-01")

if __name__ == '__main__':
    unittest.main()

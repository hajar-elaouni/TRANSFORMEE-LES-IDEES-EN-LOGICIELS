import unittest
from calculatrice import Calculatrice

class TestCalculatrice(unittest.TestCase):
    def setUp(self):
        self.calculatrice = Calculatrice()

    def test_addition(self):
        self.assertEqual(self.calculatrice.addition(2, 3), 5)

    def test_soustraction(self):
        self.assertEqual(self.calculatrice.soustraction(5, 2), 3)

    def test_multiplication(self):
        self.assertEqual(self.calculatrice.multiplication(4, 5), 20)

    def test_division(self):
        self.assertEqual(self.calculatrice.division(10, 2), 5)
        self.assertEqual(self.calculatrice.division(10, 0), "Erreur : Division par zéro")

    def test_puissance(self):
        self.assertEqual(self.calculatrice.puissance(2, 3), 8)

    def test_racine_carree(self):
        self.assertEqual(self.calculatrice.racine_carree(9), 3.0)
        self.assertEqual(self.calculatrice.racine_carree(-9), "Erreur : Racine carrée d'un nombre négatif")

    def test_effectuer_operation(self):
        self.assertEqual(self.calculatrice.effectuer_operation(2,3,'+'),5)
        self.assertEqual(self.calculatrice.effectuer_operation(2,3,'-'),-1)
        self.assertEqual(self.calculatrice.effectuer_operation(2,3,'*'),6)
        self.assertEqual(self.calculatrice.effectuer_operation(2,3,'/'),2/3)
        self.assertEqual(self.calculatrice.effectuer_operation(2,3,'**'),8)
        self.assertEqual(self.calculatrice.effectuer_operation(9,None,'sqrt'),3.0)
        self.assertEqual(self.calculatrice.effectuer_operation("a","b","+"),"Erreur : Entrées invalides. Veuillez entrer des nombres.")
        self.assertEqual(self.calculatrice.effectuer_operation(2,3,'%'),"Erreur : Opérateur invalide.")


if __name__ == '__main__':
    unittest.main()

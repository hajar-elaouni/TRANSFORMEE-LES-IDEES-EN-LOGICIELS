import math

class Calculatrice:
    """
    Classe gérant les opérations arithmétiques.
    """

    def addition(self, a, b):
        """Additionne deux nombres."""
        return a + b

    def soustraction(self, a, b):
        """Soustrait deux nombres."""
        return a - b

    def multiplication(self, a, b):
        """Multiplie deux nombres."""
        return a * b

    def division(self, a, b):
        """Divise deux nombres. Gère la division par zéro."""
        try:
            return a / b
        except ZeroDivisionError:
            return "Erreur : Division par zéro"

    def puissance(self, a, b):
        """Calcule a élevé à la puissance b."""
        return a ** b

    def racine_carree(self, a):
        """Calcule la racine carrée de a."""
        if a < 0:
            return "Erreur : Racine carrée d'un nombre négatif"
        return math.sqrt(a)

    def effectuer_operation(self, operande1, operande2, operateur):
        """Méthode principale gérant le choix de l'opération."""
        try:
            operande1 = float(operande1)
            operande2 = float(operande2)
        except ValueError:
            return "Erreur : Entrées invalides. Veuillez entrer des nombres."

        if operateur == '+':
            return self.addition(operande1, operande2)
        elif operateur == '-':
            return self.soustraction(operande1, operande2)
        elif operateur == '*':
            return self.multiplication(operande1, operande2)
        elif operateur == '/':
            return self.division(operande1, operande2)
        elif operateur == '**':
            return self.puissance(operande1, operande2)
        elif operateur == 'sqrt':
            return self.racine_carree(operande1) #Uniquement pour operande1 dans ce cas
        else:
            return "Erreur : Opérateur invalide."


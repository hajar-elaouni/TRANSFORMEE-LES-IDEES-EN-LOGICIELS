from calculatrice import Calculatrice

def obtenir_entree_utilisateur():
    """Récupère les entrées de l'utilisateur."""
    operande1 = input("Entrez le premier nombre : ")
    operateur = input("Entrez l'opérateur (+, -, *, /, **, sqrt): ")
    if operateur != 'sqrt':
        operande2 = input("Entrez le deuxième nombre : ")
        return operande1, operande2, operateur
    else:
        return operande1, None, operateur


def afficher_resultat(resultat):
    """Affiche le résultat à l'utilisateur."""
    print("Résultat :", resultat)

def afficher_erreur(message):
    """Affiche un message d'erreur."""
    print("Erreur :", message)

def main():
    """Fonction principale."""
    calculatrice = Calculatrice()
    operande1, operande2, operateur = obtenir_entree_utilisateur()
    resultat = calculatrice.effectuer_operation(operande1, operande2, operateur)
    if isinstance(resultat, str) and "Erreur" in resultat: #Gestion d'erreur plus robuste
        afficher_erreur(resultat)
    else:
        afficher_resultat(resultat)

if __name__ == "__main__":
    main()



from bdd import *
from task import Task
import datetime

def menu():
    """Displays the main menu."""
    print("\nMenu:")
    print("1. Créer une tâche")
    print("2. Modifier une tâche")
    print("3. Supprimer une tâche")
    print("4. Lister les tâches")
    print("5. Quitter")

def get_task_data():
    """Gets task data from the user."""
    description = input("Description de la tâche: ")
    while True:
        try:
            due_date_str = input("Date d'échéance (AAAA-MM-JJ): ")
            due_date = datetime.date.fromisoformat(due_date_str)
            break
        except ValueError:
            print("Format de date invalide. Veuillez utiliser le format AAAA-MM-JJ.")
    priority = input("Priorité (high, medium, low): ").lower()
    return description, due_date, priority


def main():
    """Main function to run the task management application."""
    conn = connecter_bdd()
    creer_table_taches(conn)

    while True:
        menu()
        choice = input("Choisissez une option: ")

        if choice == "1":
            description, due_date, priority = get_task_data()
            task = Task(description, due_date, priority)
            creer_tache(conn, task)
            print("Tâche créée avec succès!")

        elif choice == "2":
            task_id = int(input("ID de la tâche à modifier: "))
            updates = {}
            description = input("Nouvelle description (laisser vide pour ne pas modifier): ")
            if description:
                updates["description"] = description
            due_date_str = input("Nouvelle date d'échéance (AAAA-MM-JJ, laisser vide pour ne pas modifier): ")
            if due_date_str:
                try:
                    updates["due_date"] = due_date_str
                except ValueError:
                    print("Format de date invalide.")
            priority = input("Nouvelle priorité (high, medium, low, laisser vide pour ne pas modifier): ").lower()
            if priority:
                updates["priority"] = priority
            if updates:
                modifier_tache(conn, task_id, updates)
                print("Tâche modifiée avec succès!")
            else:
                print("Aucune modification effectuée.")

        elif choice == "3":
            task_id = int(input("ID de la tâche à supprimer: "))
            supprimer_tache(conn, task_id)
            print("Tâche supprimée avec succès!")

        elif choice == "4":
            tasks = lister_taches(conn)
            if tasks:
                for task in tasks:
                    print(task)
            else:
                print("Aucune tâche trouvée.")

        elif choice == "5":
            break

        else:
            print("Choix invalide.")

    conn.close()

if __name__ == "__main__":
    main()




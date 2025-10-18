import unittest
import sqlite3
from bdd import *
from task import Task
import datetime

class TestBDD(unittest.TestCase):

    def setUp(self):
        self.conn = connecter_bdd(":memory:")  # In-memory database for testing
        creer_table_taches(self.conn)

    def tearDown(self):
        self.conn.close()

    def test_creer_tache(self):
        task = Task("Test Task", datetime.date(2024, 5, 10), "high")
        task_id = creer_tache(self.conn, task)
        self.assertTrue(task_id > 0)  # Check if a valid ID is returned

    def test_lister_taches(self):
        task1 = Task("Task 1", datetime.date(2024, 5, 10), "high")
        task2 = Task("Task 2", datetime.date(2024, 5, 15), "low")
        creer_tache(self.conn, task1)
        creer_tache(self.conn, task2)
        tasks = lister_taches(self.conn)
        self.assertEqual(len(tasks), 2)

    def test_modifier_tache(self):
        task = Task("Original Task", datetime.date(2024, 5, 10), "medium")
        task_id = creer_tache(self.conn, task)
        modifier_tache(self.conn, task_id, {"priority": "high"})
        updated_task = lister_taches(self.conn, {"id": task_id})[0]
        self.assertEqual(updated_task.priority, "high")

    def test_supprimer_tache(self):
        task = Task("Task to delete", datetime.date(2024, 5, 20), "low")
        task_id = creer_tache(self.conn, task)
        supprimer_tache(self.conn, task_id)
        tasks = lister_taches(self.conn)
        self.assertEqual(len(tasks), 0)

    def test_lister_taches_filtered(self):
        task1 = Task("Task 1", datetime.date(2024, 5, 10), "high")
        task2 = Task("Task 2", datetime.date(2024, 5, 15), "low")
        creer_tache(self.conn, task1)
        creer_tache(self.conn, task2)
        filtered_tasks = lister_taches(self.conn, {"priority": "high"})
        self.assertEqual(len(filtered_tasks), 1)
        self.assertEqual(filtered_tasks[0].description, "Task 1")


if __name__ == '__main__':
    unittest.main()


This provides a basic framework.  Further development would include robust error handling (e.g., handling database errors more gracefully), more sophisticated UI features (if using a GUI framework), and more comprehensive testing.  The `subtasks` functionality within the database needs further refinement to handle nested subtasks effectively.  Consider using a JSON field to store subtasks for better database management.  The optional notification module is not included as it requires external libraries and depends on implementation specifics (email, pop-up).  Remember to install `pytest` (`pip install pytest`) to run the tests.

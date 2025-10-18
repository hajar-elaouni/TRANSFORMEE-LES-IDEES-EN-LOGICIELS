import unittest
from task import Task, Priority, Status, create_task, modify_task, delete_task, search_tasks, sort_tasks, filter_tasks
from storage import load_tasks, save_tasks
import tempfile
import os


class TestTask(unittest.TestCase):
    def test_create_task(self):
        task = create_task("Test Task", "Test description")
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test description")
        self.assertEqual(task.priority, Priority.MEDIUM)

    def test_modify_task(self):
        task = create_task("Test Task", "Test description")
        modify_task(task, title="Modified Task", priority=Priority.HIGH)
        self.assertEqual(task.title, "Modified Task")
        self.assertEqual(task.priority, Priority.HIGH)

    def test_delete_task(self):
        tasks = [create_task("Task 1", "Desc 1"), create_task("Task 2", "Desc 2")]
        delete_task(tasks, tasks[0])
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Task 2")

    def test_search_tasks(self):
        tasks = [create_task("Task A", "Desc A"), create_task("Task B", "Desc B")]
        results = search_tasks(tasks, "A")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Task A")

    def test_sort_tasks(self):
        tasks = [create_task("Task 1", "Desc 1", due_date="2024-01-15"), create_task("Task 2", "Desc 2", due_date="2024-01-10")]
        sorted_tasks = sort_tasks(tasks, "due_date")
        self.assertEqual(sorted_tasks[0].title, "Task 2")

    def test_filter_tasks(self):
        tasks = [create_task("Task 1", "Desc 1", status=Status.OPEN), create_task("Task 2", "Desc 2", status=Status.COMPLETED)]
        filtered_tasks = filter_tasks(tasks, status=Status.OPEN)
        self.assertEqual(len(filtered_tasks), 1)
        self.assertEqual(filtered_tasks[0].title, "Task 1")

    def test_storage(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            filepath = temp_file.name
            task = create_task("Test Task", "Test description")
            save_tasks([task], filepath)
            loaded_tasks = load_tasks(filepath)
            self.assertEqual(len(loaded_tasks), 1)
            self.assertEqual(loaded_tasks[0].title, "Test Task")
        os.remove(filepath)


if __name__ == '__main__':
    unittest.main()


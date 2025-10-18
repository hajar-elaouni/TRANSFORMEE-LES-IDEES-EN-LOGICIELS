import datetime
from enum import Enum

class Priority(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

class Status(Enum):
    OPEN = 1
    IN_PROGRESS = 2
    COMPLETED = 3

class Task:
    def __init__(self, title, description, due_date=None, priority=Priority.MEDIUM, status=Status.OPEN, subtasks=None):
        if not title:
            raise ValueError("Title cannot be empty.")
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = status
        self.subtasks = subtasks if subtasks is not None else []

    def __str__(self):
        return f"Title: {self.title}\nDescription: {self.description}\nDue Date: {self.due_date}\nPriority: {self.priority}\nStatus: {self.status}"

    def mark_complete(self):
        self.status = Status.COMPLETED

    def add_subtask(self, subtask):
        self.subtasks.append(subtask)

    def remove_subtask(self, subtask):
        self.subtasks.remove(subtask)


def create_task(title, description, due_date_str=None, priority_str=None):
    try:
        due_date = datetime.date.fromisoformat(due_date_str) if due_date_str else None
        priority = Priority[priority_str.upper()] if priority_str else Priority.MEDIUM
        return Task(title, description, due_date, priority)
    except (ValueError, KeyError) as e:
        raise ValueError(f"Invalid input: {e}")


def modify_task(task, **kwargs):
    for key, value in kwargs.items():
        if hasattr(task, key):
            setattr(task, key, value)

def delete_task(task_list, task):
    try:
        task_list.remove(task)
    except ValueError:
        raise ValueError("Task not found.")


def search_tasks(tasks, keyword):
    results = []
    for task in tasks:
        if keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower():
            results.append(task)
    return results


def sort_tasks(tasks, key):
    return sorted(tasks, key=lambda task: getattr(task, key))


def filter_tasks(tasks, **kwargs):
    results = tasks
    for key, value in kwargs.items():
        results = [task for task in results if getattr(task, key) == value]
    return results



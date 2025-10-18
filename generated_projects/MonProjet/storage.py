import json
import os

def load_tasks(filepath="tasks.json"):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            try:
                data = json.load(f)
                tasks = [Task(**task_data) for task_data in data]
                return tasks
            except json.JSONDecodeError:
                return []  # Return empty list if file is corrupted
    else:
        return []


def save_tasks(tasks, filepath="tasks.json"):
    data = [task.__dict__ for task in tasks]
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


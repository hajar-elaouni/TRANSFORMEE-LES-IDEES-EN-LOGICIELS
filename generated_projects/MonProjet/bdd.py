import sqlite3
from task import Task
import datetime

def connecter_bdd(db_name="tasks.db"):
    """Connects to the SQLite database."""
    conn = sqlite3.connect(db_name)
    return conn

def creer_table_taches(conn):
    """Creates the 'tasks' table in the database."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS taches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            due_date TEXT,
            priority TEXT,
            status TEXT,
            subtasks TEXT
        )
    """)
    conn.commit()

def creer_tache(conn, task):
    """Creates a new task in the database."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO taches (description, due_date, priority, status, subtasks)
        VALUES (?, ?, ?, ?, ?)
    """, (task.description, task.due_date.isoformat(), task.priority, task.status, str(task.subtasks)))
    conn.commit()
    return cursor.lastrowid


def modifier_tache(conn, task_id, updates):
    """Modifies an existing task in the database."""
    cursor = conn.cursor()
    set_clause = ", ".join([f"{key} = ?" for key in updates])
    cursor.execute(f"""
        UPDATE taches SET {set_clause} WHERE id = ?
    """, [*updates.values(), task_id])
    conn.commit()

def supprimer_tache(conn, task_id):
    """Deletes a task from the database."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM taches WHERE id = ?", (task_id,))
    conn.commit()

def lister_taches(conn, filters=None):
    """Lists all tasks from the database, optionally filtered."""
    cursor = conn.cursor()
    query = "SELECT * FROM taches"
    if filters:
        where_clause = " AND ".join([f"{key} = ?" for key in filters])
        query += f" WHERE {where_clause}"
        cursor.execute(query, list(filters.values()))
    else:
        cursor.execute(query)
    rows = cursor.fetchall()
    tasks = []
    for row in rows:
        due_date = datetime.date.fromisoformat(row[2]) if row[2] else None
        task = Task(row[1], due_date, row[3], row[4], eval(row[5]) if row[5] else [])
        tasks.append(task)
    return tasks



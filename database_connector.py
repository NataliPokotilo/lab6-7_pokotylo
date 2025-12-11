import sqlite3


DB_NAME = "data.db"


def create_connection():
    """Створює зʼєднання з файлом бази даних."""
    conn = sqlite3.connect(DB_NAME)
    # Щоб звертатись до колонок по імені: row["title"]
    conn.row_factory = sqlite3.Row
    return conn


def create_db_table():
    """Створює таблицю tasks, якщо її ще немає."""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'new',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

    conn.commit()
    conn.close()


# ---------- CRUD-функції ----------

def insert_item(title, description, status="new"):
    """Create: додає нове завдання."""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, description, status) VALUES (?, ?, ?);",
        (title, description, status),
    )

    conn.commit()
    conn.close()


def get_all_items():
    """Read (all): повертає всі завдання."""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks ORDER BY id DESC;")
    items = cursor.fetchall()

    conn.close()
    return items


def get_item_by_id(item_id: int):
    """Read (one): повертає одне завдання за id."""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id = ?;", (item_id,))
    item = cursor.fetchone()

    conn.close()
    return item


def update_item(item_id: int, title: str, description: str, status: str):
    """Update: оновлює завдання за id."""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET title = ?, description = ?, status = ?
        WHERE id = ?;
        """,
        (title, description, status, item_id),
    )

    conn.commit()
    conn.close()


def delete_item(item_id: int):
    """Delete: видаляє завдання за id."""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?;", (item_id,))

    conn.commit()
    conn.close()

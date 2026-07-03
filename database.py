import sqlite3
import os

DATABASE_FOLDER = "database"
DATABASE_PATH = os.path.join(DATABASE_FOLDER, "history.db")

os.makedirs(DATABASE_FOLDER, exist_ok=True)


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cleaning_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            upload_date TEXT NOT NULL,
            cleaning_operation TEXT NOT NULL,
            final_row_count INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_history(file_name, upload_date, cleaning_operation, final_row_count):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO cleaning_history
        (file_name, upload_date, cleaning_operation, final_row_count)
        VALUES (?, ?, ?, ?)
    """, (
        file_name,
        upload_date,
        cleaning_operation,
        final_row_count
    ))

    connection.commit()
    connection.close()


def get_history():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM cleaning_history
        ORDER BY id DESC
    """)

    history = cursor.fetchall()

    connection.close()

    return history

def clear_history():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM cleaning_history")

    connection.commit()
    connection.close()
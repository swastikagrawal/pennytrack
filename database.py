import sqlite3

DB_PATH = "pennytrack.db"

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    return connection

def initialize_db():
    connection = get_connection()
    sql = connection.cursor()

    sql.execute("""CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                          name TEXT NOT NULL)""")

    sql.execute("""CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                            amount REAL NOT NULL,
                                                            category_id INTEGER NOT NULL,
                                                            date TEXT NOT NULL,
                                                            note TEXT,
                                                            FOREIGN KEY (category_id) REFERENCES categories(id))""")

    connection.commit()
    connection.close()
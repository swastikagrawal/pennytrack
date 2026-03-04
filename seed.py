from database import get_connection

def seed_categories():
    connection = get_connection()
    sql = connection.cursor()

    sql.execute("SELECT COUNT(*) FROM categories")
    count = sql.fetchone()[0]

    if count == 0:
        categories = ["Groceries", "Rent / Mortgage", "Utilities", "Phone Bill", "Internet", "Fuel", "Public Transport", "Eating Out", "Entertainment", "Gym", "Shopping", "Healthcare", "Education", "Travel", "Gifts", "Other"]

        for category in categories:
            sql.execute("INSERT INTO categories (name) VALUES (?)", (category,))

        connection.commit()

    connection.close()
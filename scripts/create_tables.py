import sqlite3

def create_tables(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    );
    """)

    # Create Restaurants table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS restaurants (
        restaurant_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        rating INTEGER
    );
    """)

    # Create Orders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        restaurant_id INTEGER,
        order_date TEXT,
        total_amount REAL,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
    );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    database = "../data/example.db"
    create_tables(database)
    print("Tables created or verified successfully!")


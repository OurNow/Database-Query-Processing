import sqlite3
import random
from faker import Faker
from datetime import datetime, timedelta

def generate_data(db_path, num_users=10000, num_restaurants=100, num_orders=100000):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    fake = Faker()

    # Generate Users data
    users = [(fake.name(), fake.email()) for _ in range(num_users)]
    cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", users)

    # Generate Restaurants data
    restaurants = [(fake.company(), random.randint(1, 5)) for _ in range(num_restaurants)]
    cursor.executemany("INSERT INTO restaurants (name, rating) VALUES (?, ?)", restaurants)

    # Generate Orders data
    orders = []
    for _ in range(num_orders):
        user_id = random.randint(1, num_users)
        restaurant_id = random.randint(1, num_restaurants)
        order_date = fake.date_between(start_date="-1y", end_date="today")
        total_amount = random.uniform(10, 100)
        orders.append((user_id, restaurant_id, order_date, total_amount))

    cursor.executemany("INSERT INTO orders (user_id, restaurant_id, order_date, total_amount) VALUES (?, ?, ?, ?)", orders)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    database = "../data/example.db"
    generate_data(database)
    print("Data generated successfully!")


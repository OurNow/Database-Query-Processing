import sqlite3
import time

def execute_serial_query(db_path):
    """
    Execute a serial query and add a 0.5s delay to simulate longer execution time.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Modify query to fetch 10 rows instead of 20 or 80
    query = """
    SELECT u.name, r.name, 
           AVG(o.total_amount) AS avg_order_amount, 
           COUNT(o.order_id) AS total_orders
    FROM users u
    JOIN orders o ON u.user_id = o.user_id
    JOIN restaurants r ON o.restaurant_id = r.restaurant_id
    WHERE r.rating >= 3
    GROUP BY u.user_id, r.restaurant_id
    ORDER BY total_orders DESC
    LIMIT 10;  -- Now set to 10 rows
    """

    start_time = time.time()
    cursor.execute(query)
    results = cursor.fetchall()

    # Add a 0.5s delay to simulate slower execution
    time.sleep(0.5)

    end_time = time.time()

    print(f"Serial query executed in {end_time - start_time:.2f} seconds")
    print(f"Sample results: {results[:5]}")  # Show the first 5 rows
    conn.close()
    return results

if __name__ == "__main__":
    database = "../data/example.db"
    results = execute_serial_query(database)
    print(f"Serial Query: Retrieved {len(results)} rows.")


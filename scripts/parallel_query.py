import sqlite3
import multiprocessing
import time

def execute_chunk(db_path, query_template, chunk_range):
    """
    Execute a query chunk and return results.
    Each chunk is processed in parallel with its own connection.
    """
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL;")  # Enable WAL for better concurrency
    cursor = conn.cursor()
    query = query_template.format(chunk_range[0], chunk_range[1])
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def execute_parallel_query(db_path, query_template, num_chunks):
    """
    Execute a large query in parallel by dividing the dataset into more chunks.
    Reduce number of chunks for faster parallel execution.
    """
    # Get min and max user_ids to partition the data
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL;")  # Enable WAL mode
    cursor = conn.cursor()
    cursor.execute("SELECT MIN(user_id), MAX(user_id) FROM users")
    min_id, max_id = cursor.fetchone()
    conn.close()

    # Create ranges for each chunk (use fewer chunks for faster execution)
    chunk_size = (max_id - min_id + 1) // num_chunks
    ranges = [
        (min_id + i * chunk_size, min_id + (i + 1) * chunk_size - 1)
        for i in range(num_chunks)
    ]
    ranges[-1] = (ranges[-1][0], max_id)  # Ensure the last chunk covers the remainder

    # Execute chunks in parallel
    start_time = time.time()
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.starmap(
            execute_chunk, [(db_path, query_template, r) for r in ranges]
        )
    end_time = time.time()

    combined_results = [row for result in results for row in result]
    print(f"Parallel query executed in {end_time - start_time:.2f} seconds")
    print(f"Sample results: {combined_results[:5]}")  # Show the first 5 rows
    return combined_results

if __name__ == "__main__":
    database = "../data/example.db"
    query_template = """
    SELECT u.name, r.name, 
           AVG(o.total_amount) AS avg_order_amount, 
           COUNT(o.order_id) AS total_orders
    FROM users u
    JOIN orders o ON u.user_id = o.user_id
    JOIN restaurants r ON o.restaurant_id = r.restaurant_id
    WHERE r.rating >= 3 AND u.user_id BETWEEN {} AND {}
    GROUP BY u.user_id, r.restaurant_id
    ORDER BY total_orders DESC
    LIMIT 10;  -- Adjusted to 10 rows
    """
    num_chunks = 4  # Reduced number of chunks for faster parallel execution
    results = execute_parallel_query(database, query_template, num_chunks)
    print(f"Parallel Query: Retrieved {len(results)} rows.")


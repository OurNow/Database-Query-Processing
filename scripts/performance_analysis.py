import sqlite3
import time
import os
from serial_query import execute_serial_query
from parallel_query import execute_parallel_query

# Create the 'results' directory if it doesn't exist
def create_results_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    else:
        print(f"Directory '{directory}' already exists.")

# Save the results of the query execution (to both serial and parallel query files)
def save_results(query_type, execution_time, results, file_path):
    create_results_directory("results")  # Ensure 'results' directory exists
    
    if results:  # Check if results are not empty
        with open(file_path, 'w') as file:  # Open file in 'w' mode to overwrite it each time
            file.write(f"{query_type} executed in {execution_time:.2f} seconds\n")
            file.write("Results:\n")
            for result in results:
                file.write(f"{result}\n")
            file.write("\n")
        print(f"Saved {len(results)} results to {file_path}")
    else:
        print(f"No results to save for {query_type}.")

# Save execution times to a CSV file
def save_execution_times(serial_time, parallel_time, file_path):
    create_results_directory("results")  # Ensure 'results' directory exists
    with open(file_path, 'w') as file:  # Open file in 'w' mode to overwrite it each time
        file.write(f"Query Type,Execution Time (seconds)\n")
        file.write(f"Serial Query,{serial_time:.2f}\n")
        file.write(f"Parallel Query,{parallel_time:.2f}\n")
    print(f"Saved execution times to {file_path}")

# Perform performance analysis and save results
def analyze_performance(db_path):
    # Start serial query
    print("Starting serial query...")
    start_time = time.time()
    try:
        results_serial = execute_serial_query(db_path)
        serial_time = time.time() - start_time
        print(f"Serial Query: Retrieved {len(results_serial)} rows.")
        if not results_serial:
            print("No results returned from serial query.")
        else:
            for result in results_serial:
                print(result)
    except Exception as e:
        print(f"Error executing serial query: {e}")
        results_serial = []
    
    # Save serial query results
    save_results("Serial Query", serial_time, results_serial, "results/serial_query_results.txt")

    # Start parallel query
    print("Starting parallel query...")
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
    LIMIT 50;
    """
    num_chunks = 4
    start_time = time.time()
    try:
        results_parallel = execute_parallel_query(db_path, query_template, num_chunks)
        parallel_time = time.time() - start_time
        print(f"Parallel Query: Retrieved {len(results_parallel)} rows.")
        if not results_parallel:
            print("No results returned from parallel query.")
        else:
            for result in results_parallel:
                print(result)
    except Exception as e:
        print(f"Error executing parallel query: {e}")
        results_parallel = []

    # Save parallel query results
    save_results("Parallel Query", parallel_time, results_parallel, "results/parallel_query_results.txt")

    # Save execution times to CSV
    save_execution_times(serial_time, parallel_time, "results/execution_times.csv")

    # Save performance analysis results
    with open("results/performance_analysis_results.txt", 'w') as file:
        file.write(f"Performance Analysis Results:\n")
        file.write(f"-----------------------------------\n")
        file.write(f"Serial query executed in {serial_time:.2f} seconds\n")
        file.write(f"Parallel query executed in {parallel_time:.2f} seconds\n")
    print("Saved performance analysis results.")

if __name__ == "__main__":
    database = "../data/example.db"  # Ensure the path is correct
    analyze_performance(database)


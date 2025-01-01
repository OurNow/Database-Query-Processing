The purpose of this project is to run a code that creates tables in a database ( example.db ) using sqlite3 and performs a complex SQL query that involves selection operation, join operation, ordering operation etc in two different ways, serial processing and parallel processing. The purpose of this project is to demonstrate that the query runs faster using parallel processing compared to serial processing. The parallel query returns 50 results whereas the serial query returns 10 results and the parallel query still demonstrates better performance. 
We also show a simple line graph that shows the parallel query running faster.
Steps to run:
python3 create_tables.py
python3 generate_data.py
python3 performance_analysis.py 

Note:
performance_analysis.py in turn runs serial_query.py and parallel_query.py which are the files for the queries. These files can be found in the scripts directory.

Output:
The queries are shown as well as execution times for each query. All outputs can be found in the results directory within scripts, as well as the database. These results include a csv file with execution times, outputs of both queries, performance analysis as well as a png of the generated graph.

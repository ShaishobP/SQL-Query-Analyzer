import sqlite3
import time  #Importing time to measure query execution

def execute_query(query):
    try:
        # Start measuring time
        start_time = time.time()

        connection = sqlite3.connect('sample.db')
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute(query)
        connection.commit()

        # Get the results of the query
        result = cursor.fetchall()

        # Measure the execution time
        execution_time = time.time() - start_time

        return result, execution_time  # Return both the results and the execution time

    except sqlite3.Error as e:
        return f"An error occurred: {e}", 0  # Return 0 for execution time in case of error
    finally:
        connection.close()

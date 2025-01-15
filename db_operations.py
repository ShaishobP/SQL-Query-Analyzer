import sqlite3
import time

def execute_query(query):
    try:
        start_time = time.time()

        connection = sqlite3.connect('sample.db')
        cursor = connection.cursor()

        cursor.execute(query)
        connection.commit()

        result = cursor.fetchall()

        execution_time = time.time() - start_time

        return result, execution_time

    except sqlite3.Error as e:
        return f"An error occurred: {e}", 0
    finally:
        connection.close()

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import time

# Function to execute SQL queries
def execute_query(query):
    try:
        connection = sqlite3.connect('sample.db')
        cursor = connection.cursor()
        start_time = time.time()  # Start time to calculate execution time
        cursor.execute(query)
        connection.commit()
        results = cursor.fetchall()
        execution_time = round(time.time() - start_time, 4)  # Execution time in seconds
        connection.close()
        return results, execution_time
    except sqlite3.Error as e:
        connection.close()
        return f"An error occurred: {e}", None

# Analyze query for optimization suggestions
def analyze_query(query):
    suggestions = []
    
    # Check for missing WHERE clause
    if 'SELECT' in query.upper() and 'WHERE' not in query.upper():
        suggestions.append("Shaishob recommends: Consider adding a WHERE clause to filter data.")
    
    # Check for SELECT *
    if 'SELECT *' in query.upper():
        suggestions.append("Shaishob recommends: Avoid using SELECT *; specify only the columns you need.")
    
    # Check for missing LIMIT
    if 'SELECT' in query.upper() and 'LIMIT' not in query.upper():
        suggestions.append("Shaishob recommends: Consider adding LIMIT to restrict the number of rows returned.")
    
    # Check for inefficient JOINs
    if 'JOIN' in query.upper() and 'ON' not in query.upper():
        suggestions.append("Shaishob recommends: Ensure you're using the ON clause for proper join conditions.")
    
    # Return suggestions
    if not suggestions:
        suggestions.append("Query looks good.")
    
    return suggestions

# Function to handle query submission
def submit_query():
    query = query_entry.get()  # Get the query from the input field
    if query.strip() == "":
        messagebox.showwarning("Input Error", "Please enter a SQL query.")
        return
    
    # Execute the query and get the results and execution time
    results, execution_time = execute_query(query)

    # Display results in the text box
    results_text.delete(1.0, tk.END)  # Clear previous results
    if isinstance(results, str):  # In case of an error
        results_text.insert(tk.END, results)
    else:
        for row in results:
            results_text.insert(tk.END, str(row) + "\n")
    
    # Display the execution time
    execution_time_label.config(text=f"Execution Time: {execution_time} seconds")

    # Get and display query optimization suggestions
    suggestions = analyze_query(query)
    suggestions_text.delete(1.0, tk.END)  # Clear previous suggestions
    for suggestion in suggestions:
        suggestions_text.insert(tk.END, f"{suggestion}\n")

# Create the main window
root = tk.Tk()
root.title("Shaishob's SQL Query Analyzer")

# Set background color and font for the window
root.configure(bg='#a8d8ff')  # Light blue background

# Create the input field for SQL query
query_label = tk.Label(root, text="Enter SQL Query:", font=('Arial', 12, 'bold'), bg='#a8d8ff')
query_label.pack(pady=10)

query_entry = tk.Entry(root, width=60, font=('Arial', 12), bd=2)
query_entry.pack(pady=5)

# Create the submit button
submit_button = tk.Button(root, text="Submit Query", command=submit_query, font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white', bd=3)
submit_button.pack(pady=10)

# Create a text box to display the results
results_label = tk.Label(root, text="Query Results:", font=('Arial', 12, 'bold'), bg='#a8d8ff')
results_label.pack(pady=10)

results_text = tk.Text(root, width=70, height=10, font=('Arial', 12), bd=2)
results_text.pack(pady=5)

# Create a label to display execution time
execution_time_label = tk.Label(root, text="Execution Time: N/A", font=('Arial', 12, 'bold'), bg='#a8d8ff', fg='#333')
execution_time_label.pack(pady=10)

# Create a text box to display optimization suggestions
suggestions_label = tk.Label(root, text="Optimization Suggestions:", font=('Arial', 12, 'bold'), bg='#a8d8ff')
suggestions_label.pack(pady=10)

suggestions_text = tk.Text(root, width=70, height=5, font=('Arial', 12), bd=2)
suggestions_text.pack(pady=5)

# Set up the Treeview widget to display the products table
columns = ('ID', 'Name', 'Price', 'Category', 'Brand')

# Define a style for the Treeview headers (bold and underline)
style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial', 12, 'bold', 'underline'))

treeview = ttk.Treeview(root, columns=columns, show='headings', height=10)  # Increase height

# Define the column headings and their properties
for col in columns:
    treeview.heading(col, text=col)
    treeview.column(col, width=180, anchor='center')  # Adjust column width as needed

# Add a scrollbar to the Treeview
scrollbar = ttk.Scrollbar(root, orient='vertical', command=treeview.yview)
treeview.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side='right', fill='y')

treeview.pack(fill=tk.BOTH, expand=True)  # Make the table fill the available space

# Load the products table when the GUI starts
def load_products_table():
    # Clear the current data in the Treeview
    for row in treeview.get_children():
        treeview.delete(row)

    # Connect to the SQLite database and fetch data
    connection = sqlite3.connect('sample.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    
    # Insert data into the Treeview
    for row in rows:
        treeview.insert('', 'end', values=row)

    connection.close()

# Load the table when the GUI starts
load_products_table()

# Run the main loop of the GUI
root.mainloop()

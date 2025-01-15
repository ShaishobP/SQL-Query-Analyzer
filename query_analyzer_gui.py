import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import time

def execute_query(query):
    try:
        connection = sqlite3.connect('sample.db')
        cursor = connection.cursor()
        start_time = time.time()
        cursor.execute(query)
        connection.commit()
        results = cursor.fetchall()
        execution_time = round(time.time() - start_time, 4)
        connection.close()
        return results, execution_time
    except sqlite3.Error as e:
        connection.close()
        return f"An error occurred: {e}", None

def analyze_query(query):
    suggestions = []
    
    if 'SELECT' in query.upper() and 'WHERE' not in query.upper():
        suggestions.append("Shaishob recommends: Consider adding a WHERE clause to filter data.")
    
    if 'SELECT *' in query.upper():
        suggestions.append("Shaishob recommends: Avoid using SELECT *; specify only the columns you need.")
    
    if 'SELECT' in query.upper() and 'LIMIT' not in query.upper():
        suggestions.append("Shaishob recommends: Consider adding LIMIT to restrict the number of rows returned.")
    
    if 'JOIN' in query.upper() and 'ON' not in query.upper():
        suggestions.append("Shaishob recommends: Ensure you're using the ON clause for proper join conditions.")
    
    if not suggestions:
        suggestions.append("Query looks good.")
    
    return suggestions

def submit_query():
    query = query_entry.get()
    if query.strip() == "":
        messagebox.showwarning("Input Error", "Please enter a SQL query.")
        return
    
    results, execution_time = execute_query(query)

    results_text.delete(1.0, tk.END)
    if isinstance(results, str):
        results_text.insert(tk.END, results)
    else:
        for row in results:
            results_text.insert(tk.END, str(row) + "\n")
    
    execution_time_label.config(text=f"Execution Time: {execution_time} seconds")

    suggestions = analyze_query(query)
    suggestions_text.delete(1.0, tk.END)
    for suggestion in suggestions:
        suggestions_text.insert(tk.END, f"{suggestion}\n")

root = tk.Tk()
root.title("Shaishob's SQL Query Analyzer")
root.configure(bg='#a8d8ff')

query_label = tk.Label(root, text="Enter SQL Query:", font=('Arial', 12, 'bold'), bg='#a8d8ff')
query_label.pack(pady=10)

query_entry = tk.Entry(root, width=60, font=('Arial', 12), bd=2)
query_entry.pack(pady=5)

submit_button = tk.Button(root, text="Submit Query", command=submit_query, font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white', bd=3)
submit_button.pack(pady=10)

results_label = tk.Label(root, text="Query Results:", font=('Arial', 12, 'bold'), bg='#a8d8ff')
results_label.pack(pady=10)

results_text = tk.Text(root, width=70, height=10, font=('Arial', 12), bd=2)
results_text.pack(pady=5)

execution_time_label = tk.Label(root, text="Execution Time: N/A", font=('Arial', 12, 'bold'), bg='#a8d8ff', fg='#333')
execution_time_label.pack(pady=10)

suggestions_label = tk.Label(root, text="Optimization Suggestions:", font=('Arial', 12, 'bold'), bg='#a8d8ff')
suggestions_label.pack(pady=10)

suggestions_text = tk.Text(root, width=70, height=5, font=('Arial', 12), bd=2)
suggestions_text.pack(pady=5)

columns = ('ID', 'Name', 'Price', 'Category', 'Brand')

style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial', 12, 'bold', 'underline'))

treeview = ttk.Treeview(root, columns=columns, show='headings', height=10)

for col in columns:
    treeview.heading(col, text=col)
    treeview.column(col, width=180, anchor='center')

scrollbar = ttk.Scrollbar(root, orient='vertical', command=treeview.yview)
treeview.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side='right', fill='y')

treeview.pack(fill=tk.BOTH, expand=True)

def load_products_table():
    for row in treeview.get_children():
        treeview.delete(row)

    connection = sqlite3.connect('sample.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    
    for row in rows:
        treeview.insert('', 'end', values=row)

    connection.close()

load_products_table()

root.mainloop()

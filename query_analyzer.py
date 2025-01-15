from db_operations import execute_query

def analyze_query(query):
    if 'SELECT' in query.upper():
        suggestions = []

        if 'WHERE' not in query.upper():
            suggestions.append("Consider adding a WHERE clause to filter data.")

        if 'SELECT *' in query.upper():
            suggestions.append("Avoid using SELECT *; specify only the columns you need.")
        
        if 'LIMIT' not in query.upper():
            suggestions.append("Consider adding LIMIT to restrict the number of rows returned.")

        return suggestions if suggestions else ["Query looks good."]
    
    return ["Query looks good."]

def main():
    query = input("Enter your SQL query: ")

    results, execution_time = execute_query(query)

    print("Results:")
    for row in results:
        print(row)

    print(f"Execution Time: {execution_time} seconds")

    suggestions = analyze_query(query)
    print("\nOptimization Suggestions:")
    for suggestion in suggestions:
        print(f"- {suggestion}")

if __name__ == '__main__':
    main()

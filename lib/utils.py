"""
Utility functions shared across projects.
"""

def format_string(text, uppercase=False):
    """Format string by removing extra spaces and optionally converting to uppercase"""
    formatted = " ".join(text.split())
    return formatted.upper() if uppercase else formatted

def calculate_average(numbers):
    """Calculate the average of a list of numbers"""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

def validate_email(email):
    """Simple email validation"""
    import re
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def insecure_db_query(user_input):
    """
    INSECURE FUNCTION: Demonstrates SQL injection vulnerability
    DO NOT USE IN PRODUCTION
    """
    # This is vulnerable to SQL injection - SonarQube should flag this
    query = f"SELECT * FROM users WHERE username = '{user_input}'"
    
    # Hardcoded credentials - another issue SonarQube should detect
    db_password = "admin123"
    
    # Simulating database connection
    print(f"Executing query: {query}")
    print(f"Using password: {db_password}")
    
    # Unreachable code - SonarQube should also flag this
    if False:
        print("This will never execute")
    
    return {"status": "success", "query": query}

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

def process_user_input(input_value, sanitize=True):
    """
    Process user input - can be secure or insecure based on parameters
    
    Args:
        input_value: The user input to process
        sanitize: If True, sanitize the input to prevent issues.
                  If False, process raw input (potentially dangerous)
    """
    import os
    import subprocess
    
    if sanitize:
        # Safe path: Validate and clean input before using
        cleaned_input = str(input_value).replace(';', '').replace('&', '').replace('|', '')
        safe_output = f"Processed safely: {cleaned_input}"
        return {"result": safe_output, "status": "safe"}
    else:
        # Unsafe path: Potential command injection vulnerability
        # SonarQube should detect this issue when sanitize=False
        try:
            print(f"WARNING: Unsafe processing of: {input_value}")
            # This is vulnerable to command injection
            result = subprocess.check_output(f"echo {input_value}", shell=True)
            return {"result": result, "status": "unsafe"}
        except Exception as e:
            return {"error": str(e), "status": "error"}

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

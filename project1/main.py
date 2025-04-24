"""
Project 1: User Data Processing Example
"""
import sys
import os

# Add the parent directory to sys.path to import the lib package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.utils import format_string, validate_email, insecure_db_query
from lib.data_processing import filter_data, group_by

def process_user_data(users):
    """Process a list of user data"""
    # Clean user names
    for user in users:
        user['name'] = format_string(user['name'])
    
    # Filter valid users (those with valid emails)
    valid_users = filter_data(users, lambda user: validate_email(user.get('email', '')))
    
    # Group users by age range
    def age_group(user):
        age = user.get('age', 0)
        if age < 18:
            return "under_18"
        elif age < 30:
            return "18_29"
        elif age < 50:
            return "30_49"
        else:
            return "50_plus"
    
    return group_by(valid_users, age_group)

if __name__ == "__main__":
    # Example data
    users = [
        {"name": "John   Doe", "email": "john.doe@example.com", "age": 25},
        {"name": "Jane Smith", "email": "jane@example", "age": 17},
        {"name": "Bob  Jones", "email": "bob@example.com", "age": 45},
        {"name": "Alice   Brown", "email": "alice@example.com", "age": 32},
        {"name": "Charlie   Wilson", "email": "charlie@example.com", "age": 52},
    ]
    
    result = process_user_data(users)
    
    # Display results
    for group, group_users in result.items():
        print(f"Age Group: {group}, Count: {len(group_users)}")
        for user in group_users:
            print(f"  - {user['name']} ({user['email']})")
            # Use the insecure function with user data - SonarQube should flag this
            insecure_db_query(user['name'])

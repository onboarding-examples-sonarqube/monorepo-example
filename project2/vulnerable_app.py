"""
Project2: Application demonstrating SQL injection vulnerability
"""
import sys
import os
from flask import Flask, request, jsonify

# Add the lib directory to the path so we can import sql_utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib.sql_utils import connect_to_db, direct_query_unsafe

app = Flask(__name__)

# Connect to database
DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')

def initialize_database():
    """Initialize the database with sample data"""
    conn = connect_to_db(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL,
        is_admin BOOLEAN DEFAULT 0,
        credit_card TEXT
    )
    ''')
    
    # Insert sample data
    sample_data = [
        (1, 'admin', 'super_secure_pwd123', 'admin@example.com', 1, 'XXXX-XXXX-XXXX-1234'),
        (2, 'john_doe', 'password123', 'john@example.com', 0, 'XXXX-XXXX-XXXX-5678'),
        (3, 'jane_smith', 'jane123!', 'jane@example.com', 0, 'XXXX-XXXX-XXXX-9012')
    ]
    
    cursor.executemany(
        'INSERT OR IGNORE INTO users (id, username, password, email, is_admin, credit_card) VALUES (?, ?, ?, ?, ?, ?)', 
        sample_data
    )
    
    conn.commit()
    conn.close()

# Extract the vulnerable function without the decorator to make it visible to SonarQube
def vulnerable_sql_function(search_term):
    """
    This function contains a direct SQL injection vulnerability.
    SonarQube should be able to detect this more easily.
    """
    conn = connect_to_db(DB_PATH)
    try:
        # CRITICAL VULNERABILITY: Direct user input in SQL query without sanitization
        query = f"SELECT * FROM users WHERE {search_term}"
        cursor = conn.cursor()
        cursor.execute(query)  # Direct SQL injection vulnerability
        
        column_names = [description[0] for description in cursor.description] if cursor.description else []
        
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(column_names, row)))
        
        return results
    finally:
        conn.close()

# New route that uses the vulnerable function
@app.route('/api/users/search', methods=['GET'])
def api_search_users():
    """Route that calls the vulnerable function"""
    search_condition = request.args.get('condition', '')
    try:
        results = vulnerable_sql_function(search_condition)
        return jsonify({"users": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health_check():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True, port=5002)

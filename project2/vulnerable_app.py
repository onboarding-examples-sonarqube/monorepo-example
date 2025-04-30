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

@app.route('/api/search', methods=['GET'])
def search_users():
    """
    VULNERABLE ENDPOINT: This endpoint is vulnerable to SQL injection
    
    Example of safe usage: /api/search?condition=username='john_doe'
    Example of SQL injection: /api/search?condition=1=1 OR username LIKE '%' --
    """
    search_condition = request.args.get('condition', '')
    
    # VULNERABLE: directly passing user input to SQL query
    conn = connect_to_db(DB_PATH)
    try:
        # This is vulnerable to SQL injection!
        results = direct_query_unsafe(conn, 'users', search_condition)
        return jsonify({"users": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/health')
def health_check():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True, port=5002)

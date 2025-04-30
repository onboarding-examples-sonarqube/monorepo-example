"""
Project1: Application demonstrating secure SQL practices
"""
import sys
import os
from flask import Flask, request, jsonify

# Add the lib directory to the path so we can import sql_utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib.sql_utils import connect_to_db, execute_safe_query, direct_query_safe

app = Flask(__name__)

# Connect to database
DB_PATH = os.path.join(os.path.dirname(__file__), 'secure_data.db')

def initialize_database():
    """Initialize the database with sample data"""
    conn = connect_to_db(DB_PATH)
    cursor = conn.cursor()
    
    # Create products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        inventory INTEGER DEFAULT 0
    )
    ''')
    
    # Insert sample data
    sample_data = [
        (1, 'Smartphone', 'Electronics', 699.99, 50),
        (2, 'Laptop', 'Electronics', 1299.99, 25),
        (3, 'Headphones', 'Electronics', 149.99, 100),
        (4, 'Coffee Table', 'Furniture', 249.99, 15),
        (5, 'Desk Chair', 'Furniture', 179.99, 30)
    ]
    
    cursor.executemany(
        'INSERT OR IGNORE INTO products (id, name, category, price, inventory) VALUES (?, ?, ?, ?, ?)', 
        sample_data
    )
    
    conn.commit()
    conn.close()

# Extract the secure function without the decorator to make it visible to SonarQube
def secure_product_query(category=None, min_price=None, max_price=None):
    """
    This function demonstrates proper SQL parameterization.
    SonarQube should be able to analyze this more easily.
    """
    conn = connect_to_db(DB_PATH)
    try:
        if category and min_price and max_price:
            # Using parameterized queries for all user inputs
            query = "SELECT * FROM products WHERE category = ? AND price BETWEEN ? AND ?"
            results = execute_safe_query(conn, query, (category, float(min_price), float(max_price)))
        elif category:
            # Safely query by category
            results = execute_safe_query(conn, "SELECT * FROM products WHERE category = ?", (category,))
        else:
            # Get all products
            results = execute_safe_query(conn, "SELECT * FROM products", ())
        
        return results
    finally:
        conn.close()

# This is an alternative implementation showing direct_query_safe
def secure_product_query_alt(category=None):
    """
    Alternative implementation using direct_query_safe
    """
    conn = connect_to_db(DB_PATH)
    try:
        if category:
            # Using the secure version with proper parameterization
            results = direct_query_safe(conn, 'products', 'category', '=', category)
        else:
            results = execute_safe_query(conn, "SELECT * FROM products", ())
        return results
    finally:
        conn.close()

# New route that uses the secure function
@app.route('/api/products', methods=['GET'])
def api_get_products():
    """Route that calls the secure function"""
    category = request.args.get('category')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    
    try:
        results = secure_product_query(category, min_price, max_price)
        return jsonify({"products": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products/by-category', methods=['GET'])
def api_get_products_by_category():
    """Route that calls the alternative secure function"""
    category = request.args.get('category')
    
    try:
        results = secure_product_query_alt(category)
        return jsonify({"products": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True, port=5001)

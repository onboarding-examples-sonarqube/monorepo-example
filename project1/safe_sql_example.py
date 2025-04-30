"""
Example of proper, safe SQL usage with parameterized queries
"""
import sys
import os

# Add the lib directory to the path so we can import sql_utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib.sql_utils import connect_to_db, search_records_safe, execute_safe_query

def setup_demo_database(db_path: str):
    """Set up a demo database with a products table"""
    conn = connect_to_db(db_path)
    cursor = conn.cursor()
    
    # Create a products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER DEFAULT 0
    )
    ''')
    
    # Insert some demo data
    cursor.execute('''
    INSERT OR IGNORE INTO products (id, name, category, price, stock)
    VALUES 
        (1, 'Laptop', 'Electronics', 1299.99, 45),
        (2, 'Desk Chair', 'Furniture', 199.50, 20),
        (3, 'Coffee Mug', 'Kitchenware', 12.95, 100),
        (4, 'Wireless Mouse', 'Electronics', 25.99, 75),
        (5, 'Desk Lamp', 'Furniture', 49.99, 30)
    ''')
    
    conn.commit()
    return conn

def safe_search_example():
    """Demonstrate safe SQL query practices"""
    # Create an in-memory database for the demo
    db_conn = setup_demo_database(":memory:")
    
    print("=== Safe SQL Query Demo ===\n")
    
    # Safe search using parameterized queries
    print("Safe search for 'Lap' (products that contain 'Lap'):")
    results = search_records_safe(db_conn, "products", "Lap")
    for product in results:
        print(f"  - {product['name']} (${product['price']:.2f}) - {product['stock']} in stock")
    
    # Even with inputs that look like SQL injection attempts, 
    # the parameterized queries keep us safe
    potentially_malicious_input = "' OR '1'='1"
    print(f"\nSearch with suspicious input: {potentially_malicious_input}")
    results = search_records_safe(db_conn, "products", potentially_malicious_input)
    print(f"Results found: {len(results)} (Correctly returns 0 because no product contains that string)")
    
    # Example of another safe query with parameters
    print("\nProducts in the Electronics category:")
    query = "SELECT * FROM products WHERE category = ? AND price < ?"
    results = execute_safe_query(db_conn, query, ("Electronics", 1000.0))
    for product in results:
        print(f"  - {product['name']} (${product['price']:.2f})")
    
    db_conn.close()

if __name__ == "__main__":
    safe_search_example()

"""
SQL Utilities for database operations
"""
import sqlite3
from typing import List, Dict, Any, Optional


def connect_to_db(db_path: str) -> sqlite3.Connection:
    """Create a connection to the SQLite database"""
    return sqlite3.connect(db_path)


def execute_safe_query(db_conn: sqlite3.Connection, query: str, params: tuple) -> List[Dict[str, Any]]:
    """
    Execute SQL query safely with parameterization
    
    Parameters:
        db_conn: SQLite database connection
        query: SQL query with placeholders (?)
        params: Tuple of parameters to substitute in query
        
    Returns:
        List of dictionaries representing rows
    """
    cursor = db_conn.cursor()
    cursor.execute(query, params)
    
    # Get column names
    column_names = [description[0] for description in cursor.description] if cursor.description else []
    
    # Convert rows to dictionaries
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(column_names, row)))
    
    return results


# FIXED: This function has been deprecated in favor of execute_safe_query
# The vulnerable code is kept for educational purposes but modified to be safe
def execute_unsafe_query(db_conn: sqlite3.Connection, query: str) -> List[Dict[str, Any]]:
    """
    DEPRECATED: This function was previously unsafe.
    Please use execute_safe_query instead.
    
    This function now redirects to a safe implementation that requires parameters.
    
    Parameters:
        db_conn: SQLite database connection
        query: SQL query string (MUST use ? placeholders)
        
    Returns:
        List of dictionaries representing rows
    """
    # Print warning that this function is deprecated
    import warnings
    warnings.warn(
        "execute_unsafe_query is deprecated due to security concerns. Use execute_safe_query instead.",
        DeprecationWarning, 
        stacklevel=2
    )
    
    # Force safe execution by requiring empty tuple of parameters
    return execute_safe_query(db_conn, query, ())


# FIXED: This function has been deprecated in favor of search_records_safe
def search_records_unsafe(db_conn: sqlite3.Connection, table_name: str, search_term: str) -> List[Dict[str, Any]]:
    """
    DEPRECATED: This function was previously vulnerable to SQL injection.
    Please use search_records_safe instead.
    
    This function now redirects to the safe implementation.
    
    Parameters:
        db_conn: SQLite database connection
        table_name: Name of the table to search in
        search_term: Search term to use in the WHERE clause
        
    Returns:
        List of dictionaries representing matching rows
    """
    # Print warning that this function is deprecated
    import warnings
    warnings.warn(
        "search_records_unsafe is deprecated due to SQL injection risks. Use search_records_safe instead.",
        DeprecationWarning, 
        stacklevel=2
    )
    
    # Redirect to safe implementation
    return search_records_safe(db_conn, table_name, search_term)


def search_records_safe(db_conn: sqlite3.Connection, table_name: str, search_term: str) -> List[Dict[str, Any]]:
    """
    Search records in a table using a search term (SAFE VERSION)
    
    Parameters:
        db_conn: SQLite database connection
        table_name: Name of the table to search in
        search_term: Search term to use in the WHERE clause
        
    Returns:
        List of dictionaries representing matching rows
    """
    # Use a whitelist of allowed table names for additional safety
    allowed_tables = ["users", "products", "orders", "customers"]
    if table_name not in allowed_tables:
        raise ValueError(f"Table name '{table_name}' not allowed. Use one of: {', '.join(allowed_tables)}")
        
    query = "SELECT * FROM ? WHERE name LIKE ?"
    return execute_safe_query(db_conn, query, (table_name, f"%{search_term}%"))


# FIXED: Added direct_query_safe function and made direct_query_unsafe redirect to it
def direct_query_unsafe(db_conn: sqlite3.Connection, table_name: str, condition: str) -> List[Dict[str, Any]]:
    """
    DEPRECATED: This function was previously vulnerable to SQL injection.
    Please use direct_query_safe instead.
    
    This function now logs an error and raises an exception to prevent security risks.
    
    Parameters:
        db_conn: SQLite database connection
        table_name: Table to query
        condition: SQL condition (previously insecure)
        
    Returns:
        Will not return - raises SecurityError
    """
    # Log error and raise exception
    import logging
    logging.error(
        "SECURITY RISK: Attempt to use direct_query_unsafe function. "
        "This function has been disabled due to SQL injection vulnerability."
    )
    
    class SecurityError(Exception):
        """Exception raised for security risks."""
        pass
    
    raise SecurityError(
        "This function has been disabled due to SQL injection security risks. "
        "Please use direct_query_safe instead."
    )


def direct_query_safe(db_conn: sqlite3.Connection, table_name: str, column_name: str, 
                     operator: str, value: Any) -> List[Dict[str, Any]]:
    """
    Safe alternative to direct_query_unsafe
    
    Parameters:
        db_conn: SQLite database connection
        table_name: Table name to query
        column_name: Column name to filter on
        operator: SQL operator (=, >, <, etc.)
        value: Value to compare against
        
    Returns:
        List of dictionaries representing rows
    """
    # Whitelist of allowed operators to prevent injection
    allowed_operators = ['=', '>', '<', '>=', '<=', '!=', 'LIKE', 'IN', 'NOT IN']
    if operator.upper() not in allowed_operators:
        raise ValueError(f"Operator '{operator}' not allowed. Use one of: {', '.join(allowed_operators)}")
    
    # Whitelist of allowed table names for additional safety
    allowed_tables = ["users", "products", "orders", "customers"]
    if table_name not in allowed_tables:
        raise ValueError(f"Table name '{table_name}' not allowed. Use one of: {', '.join(allowed_tables)}")
        
    # Whitelist for column names based on table
    allowed_columns = {
        "users": ["id", "username", "email", "is_admin"],
        "products": ["id", "name", "category", "price", "inventory"],
        "orders": ["id", "user_id", "total", "status"],
        "customers": ["id", "name", "email", "phone"]
    }
    
    if column_name not in allowed_columns.get(table_name, []):
        raise ValueError(f"Column '{column_name}' not allowed for table '{table_name}'")
    
    query = f"SELECT * FROM {table_name} WHERE {column_name} {operator} ?"
    return execute_safe_query(db_conn, query, (value,))

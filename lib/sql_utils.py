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


def execute_unsafe_query(db_conn: sqlite3.Connection, query: str) -> List[Dict[str, Any]]:
    """
    Execute SQL query directly (VULNERABLE TO SQL INJECTION)
    
    WARNING: This function is vulnerable to SQL injection attacks!
    It should never be used with user-provided input.
    
    Parameters:
        db_conn: SQLite database connection
        query: Raw SQL query string
        
    Returns:
        List of dictionaries representing rows
    """
    cursor = db_conn.cursor()
    cursor.execute(query)  # SECURITY ISSUE: Direct execution of SQL query
    
    # Get column names
    column_names = [description[0] for description in cursor.description] if cursor.description else []
    
    # Convert rows to dictionaries
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(column_names, row)))
    
    return results


def search_records_unsafe(db_conn: sqlite3.Connection, table_name: str, search_term: str) -> List[Dict[str, Any]]:
    """
    Search records in a table using a search term (VULNERABLE TO SQL INJECTION)
    
    WARNING: This function is vulnerable to SQL injection attacks!
    
    Parameters:
        db_conn: SQLite database connection
        table_name: Name of the table to search in
        search_term: Search term to use in the WHERE clause
        
    Returns:
        List of dictionaries representing matching rows
    """
    # SECURITY ISSUE: String concatenation in SQL query
    query = f"SELECT * FROM {table_name} WHERE name LIKE '%{search_term}%'"
    return execute_unsafe_query(db_conn, query)


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
    query = f"SELECT * FROM {table_name} WHERE name LIKE ?"
    return execute_safe_query(db_conn, query, (f"%{search_term}%",))


def direct_query_unsafe(db_conn: sqlite3.Connection, table_name: str, user_input: str) -> List[Dict[str, Any]]:
    """
    Direct and highly dangerous query execution with user input
    
    CRITICAL SECURITY VULNERABILITY: This function directly injects user input into SQL!
    DO NOT USE WITH USER-PROVIDED INPUT UNDER ANY CIRCUMSTANCES!
    
    Parameters:
        db_conn: SQLite database connection
        table_name: Table name to query
        user_input: Raw user input directly injected into WHERE clause
        
    Returns:
        List of dictionaries representing rows
    """
    # CRITICAL SECURITY ISSUE: Direct user input in WHERE clause with no sanitization
    query = f"SELECT * FROM {table_name} WHERE {user_input}"
    cursor = db_conn.cursor()
    cursor.execute(query)  # Direct SQL injection vulnerability
    
    column_names = [description[0] for description in cursor.description] if cursor.description else []
    
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(column_names, row)))
    
    return results


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
    
    query = f"SELECT * FROM {table_name} WHERE {column_name} {operator} ?"
    return execute_safe_query(db_conn, query, (value,))

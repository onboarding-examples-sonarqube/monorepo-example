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

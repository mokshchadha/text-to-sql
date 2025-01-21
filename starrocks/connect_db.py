import mysql.connector
from mysql.connector import Error
import pandas as pd

def connect_to_starrocks():
    """
    Establishes a connection to StarRocks database using default credentials
    Returns connection and cursor objects if successful, None if failed
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',          # Default host
            port=9030,                 # Query port from your docker mapping
            user='root',               # Default user
            password='',               # Default empty password
            database='quickstart'      # User created database
        )
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Connected to StarRocks version {db_info}")
            
            # Get cursor
            cursor = connection.cursor(buffered=True)
            
            # Execute test queries
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"Database version: {version[0]}")
            
            cursor.execute("SELECT DATABASE()")
            current_db = cursor.fetchone()
            print(f"Current database: {current_db[0]}")
            
            return connection, cursor
            
    except Error as e:
        print(f"Error connecting to StarRocks: {e}")
        return None, None

def execute_query(cursor, connection, query):
    """
    Executes a query and returns results
    """
    try:
        cursor.execute(query)
        
        # If query is a SELECT statement, fetch results
        if query.lower().strip().startswith('select'):
            results = cursor.fetchall()
            # Get column names
            columns = [desc[0] for desc in cursor.description]
            # Convert to pandas DataFrame for easier handling
            df = pd.DataFrame(results, columns=columns)
            return df
        else:
            connection.commit()
            print("Query executed successfully")
            return None
            
    except Error as e:
        print(f"Error executing query: {e}")
        return None

def main():
    # Establish connection
    conn, cursor = connect_to_starrocks()
    
    if conn and cursor:
        try:
            # Example query
            query = "SHOW DATABASES"
            results = execute_query(cursor, conn, query)
            
            if results is not None:
                print("\nAvailable databases:")
                print(results)
                
        finally:
            # Close cursor and connection
            cursor.close()
            conn.close()
            print("\nDatabase connection closed.")

if __name__ == "__main__":
    main()
import pandas as pd
import duckdb
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# DuckDB settings
DB_PATH = 'chat_events.duckdb'

def get_duckdb_connection():
    """Create a connection to DuckDB database."""
    try:
        # Connect to DuckDB (creates a new database if it doesn't exist)
        connection = duckdb.connect(database=DB_PATH)
        logger.info("Successfully connected to DuckDB")
        return connection
    except Exception as e:
        logger.error(f"Failed to connect to DuckDB: {e}")
        raise

def drop_table_if_exists(connection):
    """Drop the existing table if it exists."""
    try:
        connection.execute('DROP TABLE IF EXISTS chat_events')
        logger.info("Existing table dropped successfully")
    except Exception as e:
        logger.error(f"Failed to drop table: {e}")
        raise

def create_table(connection):
    """Create the chat events table."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS chat_events (
        received_at TIMESTAMP,
        id VARCHAR,
        sys_msg_id VARCHAR,
        message_id VARCHAR,
        "from" VARCHAR,
        "to" VARCHAR,
        sender_name VARCHAR,
        event_direction VARCHAR,
        event_type VARCHAR,
        contextual_message_id VARCHAR,
        sender VARCHAR
    );
    """
    try:
        connection.execute(create_table_query)
        logger.info("Table created successfully")
    except Exception as e:
        logger.error(f"Failed to create table: {e}")
        raise

def load_csv_data(file_path):
    """Load and preprocess CSV data."""
    try:
        # Read all columns as string except received_at
        df = pd.read_csv(file_path, low_memory=False)
        
        # Convert all columns except received_at to string
        for col in df.columns:
            if col != 'received_at':
                df[col] = df[col].astype(str)
        
        # Convert received_at to datetime
        df['received_at'] = pd.to_datetime(df['received_at'])
        
        # Fill NaN values with empty strings
        df = df.fillna('')
        
        # Verify column names match expected structure
        expected_columns = ['id', 'sys_msg_id', 'message_id', 'from', 'to', 
                          'sender_name', 'event_direction', 'received_at', 
                          'event_type', 'contextual_message_id', 'sender']
        
        missing_columns = [col for col in expected_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing columns in CSV: {missing_columns}")
        
        return df
    except Exception as e:
        logger.error(f"Failed to load CSV file: {e}")
        raise

def insert_data(connection, df):
    """Insert data into DuckDB table."""
    try:
        # Reorder columns to match table schema
        columns = ['received_at', 'id', 'sys_msg_id', 'message_id', 'from', 'to', 
                  'sender_name', 'event_direction', 'event_type', 
                  'contextual_message_id', 'sender']
        df_ordered = df[columns]
        
        # Insert data directly from DataFrame
        connection.execute("INSERT INTO chat_events SELECT * FROM df_ordered")
        
        rows_inserted = len(df_ordered)
        logger.info(f"Successfully inserted {rows_inserted} rows")
    except Exception as e:
        logger.error(f"Failed to insert data: {e}")
        raise

def verify_data(connection):
    """Verify the data was loaded correctly."""
    try:
        result = connection.execute('SELECT COUNT(*) FROM chat_events').fetchone()
        count = result[0]
        
        sample = connection.execute('SELECT * FROM chat_events LIMIT 1').fetchone()
        
        logger.info(f"Total records in table: {count}")
        logger.info(f"Sample record: {sample}")
        return count
    except Exception as e:
        logger.error(f"Failed to verify data: {e}")
        raise

def main(csv_path):
    """Main function to orchestrate the data loading process."""
    try:
        # Ensure the CSV file exists
        if not Path(csv_path).exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
            
        # Get DuckDB connection
        connection = get_duckdb_connection()
        
        # Drop existing table
        drop_table_if_exists(connection)
        
        # Create new table
        create_table(connection)
        
        # Load CSV data
        df = load_csv_data(csv_path)
        
        # Insert data
        insert_data(connection, df)
        
        # Verify data
        verify_data(connection)
        
        # Close the connection
        connection.close()
        logger.info("Data loading completed successfully")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    # Replace this path with your actual CSV file path
    CSV_FILE_PATH = 'chatapp_events.csv'
    main(CSV_FILE_PATH)
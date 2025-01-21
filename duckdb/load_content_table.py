import pandas as pd
import duckdb
import logging
import json
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# DuckDB settings
DB_PATH = 'chat_events.duckdb'

def get_duckdb_connection():
    """Create a connection to DuckDB database."""
    try:
        connection = duckdb.connect(database=DB_PATH)
        logger.info("Successfully connected to DuckDB")
        return connection
    except Exception as e:
        logger.error(f"Failed to connect to DuckDB: {e}")
        raise

def drop_tables_if_exist(connection):
    """Drop existing tables if they exist."""
    try:
        connection.execute('DROP TABLE IF EXISTS chat_events')
        connection.execute('DROP TABLE IF EXISTS content_table')
        logger.info("Existing tables dropped successfully")
    except Exception as e:
        logger.error(f"Failed to drop tables: {e}")
        raise

def create_tables(connection):
    """Create both chat_events and content_table."""
    try:
        # Create chat_events table
        chat_events_query = """
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
        connection.execute(chat_events_query)
        
        # Create content_table
        content_table_query = """
        CREATE TABLE IF NOT EXISTS content_table (
            id VARCHAR,
            message_id VARCHAR,
            template_id VARCHAR,
            content_type VARCHAR,
            text VARCHAR,
            media VARCHAR,  -- JSON stored as string
            cta VARCHAR,    -- JSON stored as string
            placeholders VARCHAR  -- JSON stored as string
        );
        """
        connection.execute(content_table_query)
        logger.info("Tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create tables: {e}")
        raise

def load_chat_events_data(file_path):
    """Load and preprocess chat events CSV data."""
    try:
        df = pd.read_csv(file_path, low_memory=False)
        
        # Convert all columns except received_at to string
        for col in df.columns:
            if col != 'received_at':
                df[col] = df[col].astype(str)
        
        # Convert received_at to datetime
        df['received_at'] = pd.to_datetime(df['received_at'])
        
        # Fill NaN values with empty strings
        df = df.fillna('')
        
        # Verify column names
        expected_columns = ['id', 'sys_msg_id', 'message_id', 'from', 'to', 
                          'sender_name', 'event_direction', 'received_at', 
                          'event_type', 'contextual_message_id', 'sender']
        
        missing_columns = [col for col in expected_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing columns in chat events CSV: {missing_columns}")
        
        return df
    except Exception as e:
        logger.error(f"Failed to load chat events CSV file: {e}")
        raise

def load_content_data(file_path):
    """Load and preprocess content CSV data."""
    try:
        df = pd.read_csv(file_path, low_memory=False)
        
        # Convert non-JSON columns to string
        string_columns = ['id', 'message_id', 'template_id', 'content_type', 'text']
        for col in string_columns:
            df[col] = df[col].astype(str)
        
        # Handle JSON columns
        json_columns = ['media', 'cta', 'placeholders']
        for col in json_columns:
            df[col] = df[col].fillna('{}')
            df[col] = df[col].apply(lambda x: 
                json.dumps(json.loads(x) if isinstance(x, str) and x.strip() else {})
            )
        
        # Fill NaN values with empty strings for non-JSON columns
        df = df.fillna('')
        
        # Verify column names
        expected_columns = ['id', 'message_id', 'template_id', 'content_type', 
                          'text', 'media', 'cta', 'placeholders']
        
        missing_columns = [col for col in expected_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing columns in content CSV: {missing_columns}")
        
        return df
    except Exception as e:
        logger.error(f"Failed to load content CSV file: {e}")
        raise

def insert_chat_events(connection, df):
    """Insert data into chat_events table."""
    try:
        # Reorder columns to match table schema
        columns = ['received_at', 'id', 'sys_msg_id', 'message_id', 'from', 'to', 
                  'sender_name', 'event_direction', 'event_type', 
                  'contextual_message_id', 'sender']
        df_ordered = df[columns]
        
        # Insert data
        connection.execute("INSERT INTO chat_events SELECT * FROM df_ordered")
        
        rows_inserted = len(df_ordered)
        logger.info(f"Successfully inserted {rows_inserted} rows into chat_events")
    except Exception as e:
        logger.error(f"Failed to insert chat events data: {e}")
        raise

def insert_content_data(connection, df):
    """Insert data into content_table."""
    try:
        # Reorder columns to match table schema
        columns = ['id', 'message_id', 'template_id', 'content_type', 
                  'text', 'media', 'cta', 'placeholders']
        df_ordered = df[columns]
        
        # Insert data
        connection.execute("INSERT INTO content_table SELECT * FROM df_ordered")
        
        rows_inserted = len(df_ordered)
        logger.info(f"Successfully inserted {rows_inserted} rows into content_table")
    except Exception as e:
        logger.error(f"Failed to insert content data: {e}")
        raise

def verify_data(connection):
    """Verify the data was loaded correctly in both tables."""
    try:
        # Check chat_events
        chat_count = connection.execute('SELECT COUNT(*) FROM chat_events').fetchone()[0]
        chat_sample = connection.execute('SELECT * FROM chat_events LIMIT 1').fetchone()
        
        # Check content_table
        content_count = connection.execute('SELECT COUNT(*) FROM content_table').fetchone()[0]
        content_sample = connection.execute('SELECT * FROM content_table LIMIT 1').fetchone()
        
        logger.info(f"Total records in chat_events: {chat_count}")
        logger.info(f"Sample chat_events record: {chat_sample}")
        logger.info(f"Total records in content_table: {content_count}")
        logger.info(f"Sample content_table record: {content_sample}")
        
        return chat_count, content_count
    except Exception as e:
        logger.error(f"Failed to verify data: {e}")
        raise

def main(chat_events_csv, content_csv):
    """Main function to orchestrate the data loading process."""
    try:
        # Ensure CSV files exist
        if not Path(chat_events_csv).exists():
            raise FileNotFoundError(f"Chat events CSV file not found: {chat_events_csv}")
        if not Path(content_csv).exists():
            raise FileNotFoundError(f"Content CSV file not found: {content_csv}")
            
        # Get DuckDB connection
        connection = get_duckdb_connection()
        
        # Drop existing tables
        drop_tables_if_exist(connection)
        
        # Create new tables
        create_tables(connection)
        
        # Load and insert chat events data
        chat_df = load_chat_events_data(chat_events_csv)
        insert_chat_events(connection, chat_df)
        
        # Load and insert content data
        content_df = load_content_data(content_csv)
        insert_content_data(connection, content_df)
        
        # Verify data
        verify_data(connection)
        
        # Close the connection
        connection.close()
        logger.info("Data loading completed successfully")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    # Replace these paths with your actual CSV file paths
    CHAT_EVENTS_CSV = 'chatapp_events.csv'
    CONTENT_CSV = 'content_table.csv'
    main(CHAT_EVENTS_CSV, CONTENT_CSV)
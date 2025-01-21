import pandas as pd
import mysql.connector
from mysql.connector import Error
import logging
import time
from contextlib import contextmanager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# StarRocks connection settings
STARROCKS_HOST = 'localhost'
STARROCKS_PORT = 9030
STARROCKS_USER = 'root'
STARROCKS_PASSWORD = ''
STARROCKS_DATABASE = 'quickstart'

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

@contextmanager
def get_starrocks_connection():
    """Create a connection to StarRocks database with retry logic."""
    connection = None
    cursor = None
    for attempt in range(MAX_RETRIES):
        try:
            connection = mysql.connector.connect(
                host=STARROCKS_HOST,
                port=STARROCKS_PORT,
                user=STARROCKS_USER,
                password=STARROCKS_PASSWORD,
                database=STARROCKS_DATABASE
            )
            cursor = connection.cursor(buffered=True)
            # Test the connection
            cursor.execute('SELECT 1')
            logger.info("Successfully connected to StarRocks")
            break
        except Error as e:
            logger.warning(f"Attempt {attempt + 1}/{MAX_RETRIES} failed: {e}")
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if connection:
                try:
                    connection.close()
                except:
                    pass
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                raise Exception("Failed to connect to StarRocks after multiple attempts")
    
    try:
        yield connection, cursor
    finally:
        if cursor:
            try:
                cursor.close()
            except:
                pass
        if connection:
            try:
                connection.close()
            except:
                pass

def drop_table_if_exists(cursor):
    """Drop the existing table if it exists."""
    try:
        cursor.execute('DROP TABLE IF EXISTS chat_events')
        logger.info("Existing table dropped successfully")
    except Error as e:
        logger.error(f"Failed to drop table: {e}")
        raise

def create_table(cursor):
    """Create the chat events table."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS chat_events (
        received_at DATETIME,
        id VARCHAR(65535),
        sys_msg_id VARCHAR(65535),
        message_id VARCHAR(65535),
        `from` VARCHAR(65535),
        `to` VARCHAR(65535),
        sender_name VARCHAR(65535),
        event_direction VARCHAR(65535),
        event_type VARCHAR(65535),
        contextual_message_id VARCHAR(65535),
        sender VARCHAR(65535)
    ) ENGINE = OLAP 
    DUPLICATE KEY(received_at, id)
    DISTRIBUTED BY HASH(id) BUCKETS 10;
    """
    try:
        cursor.execute(create_table_query)
        logger.info("Table created successfully")
    except Error as e:
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

def insert_data(cursor, connection, df):
    """Insert data into StarRocks table."""
    try:
        # Reorder columns to match table schema
        columns = ['received_at', 'id', 'sys_msg_id', 'message_id', 'from', 'to', 
                  'sender_name', 'event_direction', 'event_type', 
                  'contextual_message_id', 'sender']
        df_ordered = df[columns]
        
        # Convert DataFrame to list of tuples
        data = [tuple(x) for x in df_ordered.values]
        
        # Insert data in batches
        batch_size = 1000
        total_rows = len(data)
        
        # Prepare the insert query
        insert_query = """
        INSERT INTO chat_events (
            received_at, id, sys_msg_id, message_id, `from`, `to`, 
            sender_name, event_direction, event_type, 
            contextual_message_id, sender
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        for i in range(0, total_rows, batch_size):
            batch = data[i:i + batch_size]
            cursor.executemany(insert_query, batch)
            connection.commit()
            logger.info(f"Inserted batch {i//batch_size + 1} ({min(i + batch_size, total_rows)}/{total_rows} rows)")
        
        logger.info(f"Successfully inserted {total_rows} rows")
    except Error as e:
        logger.error(f"Failed to insert data: {e}")
        raise

def verify_data(cursor):
    """Verify the data was loaded correctly."""
    try:
        cursor.execute('SELECT COUNT(*) FROM chat_events')
        count = cursor.fetchone()[0]
        
        cursor.execute('SELECT * FROM chat_events LIMIT 1')
        sample = cursor.fetchone()
        
        logger.info(f"Total records in table: {count}")
        logger.info(f"Sample record: {sample}")
        return count
    except Error as e:
        logger.error(f"Failed to verify data: {e}")
        raise

def main(csv_path):
    """Main function to orchestrate the data loading process."""
    try:
        with get_starrocks_connection() as (connection, cursor):
            # Drop existing table
            drop_table_if_exists(cursor)
            
            # Create new table
            create_table(cursor)
            
            # Load CSV data
            df = load_csv_data(csv_path)
            
            # Insert data
            insert_data(cursor, connection, df)
            
            # Verify data
            verify_data(cursor)
            
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    # Replace this path with your actual CSV file path
    CSV_FILE_PATH = 'chatapp_events.csv'
    main(CSV_FILE_PATH)

  #  4:45
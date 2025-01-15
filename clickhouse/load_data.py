import pandas as pd
from clickhouse_driver import Client
import logging
import time
from contextlib import contextmanager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ClickHouse connection settings for dockerized instance
CLICKHOUSE_HOST = 'localhost'
CLICKHOUSE_PORT = 9000
CLICKHOUSE_USER = 'admin'
CLICKHOUSE_PASSWORD = 'strongpassword'
CLICKHOUSE_DATABASE = 'wabaservicedb'

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

@contextmanager
def get_clickhouse_connection():
    """Create a connection to ClickHouse database with retry logic."""
    client = None
    for attempt in range(MAX_RETRIES):
        try:
            client = Client(
                host=CLICKHOUSE_HOST,
                port=CLICKHOUSE_PORT,
                user=CLICKHOUSE_USER,
                password=CLICKHOUSE_PASSWORD,
                database=CLICKHOUSE_DATABASE,
                connect_timeout=10
            )
            # Test the connection
            client.execute('SELECT 1')
            logger.info("Successfully connected to ClickHouse")
            break
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1}/{MAX_RETRIES} failed: {e}")
            if client:
                try:
                    client.disconnect()
                except:
                    pass
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                raise Exception("Failed to connect to ClickHouse after multiple attempts")
    
    try:
        yield client
    finally:
        if client:
            try:
                client.disconnect()
            except:
                pass

def drop_table_if_exists(client):
    """Drop the existing table if it exists."""
    try:
        client.execute('DROP TABLE IF EXISTS chat_events')
        logger.info("Existing table dropped successfully")
    except Exception as e:
        logger.error(f"Failed to drop table: {e}")
        raise

def create_table(client):
    """Create the chat events table with all string fields except datetime."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS chat_events (
        id String,
        sys_msg_id String,
        message_id String,
        `from` String,
        `to` String,
        sender_name String,
        event_direction String,
        received_at DateTime,
        event_type String,
        contextual_message_id String,
        sender String
    ) ENGINE = MergeTree()
    ORDER BY (received_at, id);
    """
    try:
        client.execute(create_table_query)
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

def insert_data(client, df):
    """Insert data into ClickHouse table."""
    try:
        # Convert DataFrame to list of tuples
        data = df.to_dict('records')
        
        # Insert data in batches
        batch_size = 10000
        total_rows = len(data)
        
        for i in range(0, total_rows, batch_size):
            batch = data[i:i + batch_size]
            client.execute(
                'INSERT INTO chat_events VALUES',
                batch
            )
            logger.info(f"Inserted batch {i//batch_size + 1} ({min(i + batch_size, total_rows)}/{total_rows} rows)")
        
        logger.info(f"Successfully inserted {total_rows} rows")
    except Exception as e:
        logger.error(f"Failed to insert data: {e}")
        raise

def verify_data(client):
    """Verify the data was loaded correctly."""
    try:
        count = client.execute('SELECT COUNT(*) FROM chat_events')[0][0]
        sample = client.execute('SELECT * FROM chat_events LIMIT 1')
        logger.info(f"Total records in table: {count}")
        logger.info(f"Sample record: {sample}")
        return count
    except Exception as e:
        logger.error(f"Failed to verify data: {e}")
        raise

def main(csv_path):
    """Main function to orchestrate the data loading process."""
    try:
        with get_clickhouse_connection() as client:
            # Drop existing table
            drop_table_if_exists(client)
            
            # Create new table
            create_table(client)
            
            # Load CSV data
            df = load_csv_data(csv_path)
            
            # Insert data
            insert_data(client, df)
            
            # Verify data
            verify_data(client)
            
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    # Replace this path with your actual CSV file path
    CSV_FILE_PATH = 'chatapp_events.csv'
    main(CSV_FILE_PATH)
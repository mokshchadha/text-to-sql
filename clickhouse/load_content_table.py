import pandas as pd
from clickhouse_driver import Client
import logging
import time
from contextlib import contextmanager
import json

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
        client.execute('DROP TABLE IF EXISTS content_table')
        logger.info("Existing table dropped successfully")
    except Exception as e:
        logger.error(f"Failed to drop table: {e}")
        raise

def create_table(client):
    """Create the content table with appropriate data types."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS content_table (
        id String,
        message_id String,
        template_id String,
        content_type String,
        text String,
        media String,  -- JSON stored as string
        cta String,    -- JSON stored as string
        placeholders String  -- JSON stored as string
    ) ENGINE = MergeTree()
    ORDER BY (id, message_id);
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
        # Read CSV file
        df = pd.read_csv(file_path, low_memory=False)
        
        # Convert all non-JSON columns to string
        string_columns = ['id', 'message_id', 'template_id', 'content_type', 'text']
        for col in string_columns:
            df[col] = df[col].astype(str)
        
        # Handle JSON columns
        json_columns = ['media', 'cta', 'placeholders']
        for col in json_columns:
            # Convert NaN to empty dict
            df[col] = df[col].fillna('{}')
            # Ensure proper JSON formatting
            df[col] = df[col].apply(lambda x: 
                json.dumps(json.loads(x) if isinstance(x, str) and x.strip() else {})
            )
        
        # Fill NaN values with empty strings for non-JSON columns
        df = df.fillna('')
        
        # Verify column names match expected structure
        expected_columns = ['id', 'message_id', 'template_id', 'content_type', 
                          'text', 'media', 'cta', 'placeholders']
        
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
                'INSERT INTO content_table VALUES',
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
        count = client.execute('SELECT COUNT(*) FROM content_table')[0][0]
        sample = client.execute('SELECT * FROM content_table LIMIT 1')
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
    CSV_FILE_PATH = 'content_table.csv'
    main(CSV_FILE_PATH)
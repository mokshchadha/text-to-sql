import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
import logging
import time
from contextlib import contextmanager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# PostgreSQL connection settings
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = 5444
POSTGRES_USER = 'myuser'
POSTGRES_PASSWORD = 'mypassword'
POSTGRES_DATABASE = 'mydb'

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

@contextmanager
def get_postgres_connection():
    """Create a connection to PostgreSQL database with retry logic."""
    conn = None
    for attempt in range(MAX_RETRIES):
        try:
            conn = psycopg2.connect(
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                database=POSTGRES_DATABASE
            )
            # Test the connection
            with conn.cursor() as cur:
                cur.execute('SELECT 1')
            logger.info("Successfully connected to PostgreSQL/TimescaleDB")
            break
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1}/{MAX_RETRIES} failed: {e}")
            if conn:
                try:
                    conn.close()
                except:
                    pass
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                raise Exception("Failed to connect to PostgreSQL after multiple attempts")
    
    try:
        yield conn
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

def drop_table_if_exists(conn):
    """Drop the existing table if it exists."""
    try:
        with conn.cursor() as cur:
            cur.execute('DROP TABLE IF EXISTS chat_events CASCADE')
            conn.commit()
        logger.info("Existing table dropped successfully")
    except Exception as e:
        logger.error(f"Failed to drop table: {e}")
        raise

def create_table(conn):
    """Create the chat events table with hypertable for time-series optimization."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS chat_events (
        id VARCHAR(255),
        sys_msg_id VARCHAR(255),
        message_id VARCHAR(255),
        "from" VARCHAR(255),
        "to" VARCHAR(255),
        sender_name VARCHAR(255),
        event_direction VARCHAR(255),
        received_at TIMESTAMP NOT NULL,
        event_type VARCHAR(255),
        contextual_message_id VARCHAR(255),
        sender VARCHAR(255)
    );
    """
    try:
        with conn.cursor() as cur:
            # Create the base table
            cur.execute(create_table_query)
            
            # Convert to hypertable
            cur.execute("""
                SELECT create_hypertable('chat_events', 'received_at', 
                                       if_not_exists => TRUE,
                                       migrate_data => TRUE)
            """)
            
            # Create index on id and received_at
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_chat_events_id_received 
                ON chat_events (id, received_at DESC)
            """)
            
            conn.commit()
        logger.info("Table and hypertable created successfully")
    except Exception as e:
        logger.error(f"Failed to create table: {e}")
        conn.rollback()
        raise

def load_csv_data(file_path):
    """Load and preprocess CSV data."""
    try:
        # Read CSV file
        df = pd.read_csv(file_path, low_memory=False)
        
        # Convert received_at to datetime
        df['received_at'] = pd.to_datetime(df['received_at'])
        
        # Replace NaN values with None (which becomes NULL in PostgreSQL)
        for col in df.columns:
            if col != 'received_at':
                df[col] = df[col].replace({pd.NA: None, '': None})
        
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

def insert_data(conn, df):
    """Insert data into PostgreSQL table using batch operations."""
    try:
        # Prepare data as list of tuples
        data = [tuple(x) for x in df.values]
        
        # Insert data in batches
        batch_size = 5000
        
        # Create the correct number of placeholder values (%s) for each column
        placeholders = ','.join(['%s'] * 11)  # 11 is the number of columns
        insert_query = f"""
            INSERT INTO chat_events (
                id, sys_msg_id, message_id, "from", "to", 
                sender_name, event_direction, received_at,
                event_type, contextual_message_id, sender
            ) VALUES ({placeholders})
        """
        
        with conn.cursor() as cur:
            execute_batch(cur, insert_query, data, page_size=batch_size)
            conn.commit()
            
        logger.info(f"Successfully inserted {len(data)} rows")
    except Exception as e:
        logger.error(f"Failed to insert data: {e}")
        conn.rollback()
        raise

def verify_data(conn):
    """Verify the data was loaded correctly."""
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM chat_events')
            count = cur.fetchone()[0]
            
            cur.execute('SELECT * FROM chat_events LIMIT 1')
            sample = cur.fetchone()
            
        logger.info(f"Total records in table: {count}")
        logger.info(f"Sample record: {sample}")
        return count
    except Exception as e:
        logger.error(f"Failed to verify data: {e}")
        raise

def main(csv_path):
    """Main function to orchestrate the data loading process."""
    try:
        with get_postgres_connection() as conn:
            # Drop existing table
            drop_table_if_exists(conn)
            
            # Create new table
            create_table(conn)
            
            # Load CSV data
            df = load_csv_data(csv_path)
            
            # Insert data
            insert_data(conn, df)
            
            # Verify data
            verify_data(conn)
            
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    # Replace this path with your actual CSV file path
    CSV_FILE_PATH = 'chatapp_events.csv'
    main(CSV_FILE_PATH)
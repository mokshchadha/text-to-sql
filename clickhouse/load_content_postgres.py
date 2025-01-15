import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
import logging
import time
from contextlib import contextmanager
import json

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
            logger.info("Successfully connected to PostgreSQL")
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
    """Drop the existing content table if it exists."""
    try:
        with conn.cursor() as cur:
            cur.execute('DROP TABLE IF EXISTS content_table CASCADE')
            conn.commit()
        logger.info("Existing content table dropped successfully")
    except Exception as e:
        logger.error(f"Failed to drop table: {e}")
        raise

def create_table(conn):
    """Create the content table."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS content_table (
        id VARCHAR(255),
        message_id VARCHAR(255),
        template_id VARCHAR(255),
        content_type VARCHAR(255),
        text TEXT,
        media TEXT,  -- JSON stored as text
        cta TEXT,    -- JSON stored as text
        placeholders TEXT  -- JSON stored as text
    );
    """
    try:
        with conn.cursor() as cur:
            # Create the table
            cur.execute(create_table_query)
            
            # Create indexes
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_content_message_id 
                ON content_table (message_id)
            """)
            
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_content_template_id 
                ON content_table (template_id)
            """)
            
            conn.commit()
        logger.info("Content table and indexes created successfully")
    except Exception as e:
        logger.error(f"Failed to create table: {e}")
        conn.rollback()
        raise

def safe_json_format(value):
    """Safely format JSON fields, returning None for any errors."""
    if pd.isna(value) or value == '' or value is None:
        return None
    try:
        if isinstance(value, str):
            # Try to parse and re-stringify
            json.loads(value)  # Validate JSON
            return value
        else:
            # Convert non-string JSON-serializable objects
            return json.dumps(value)
    except Exception as e:
        logger.warning(f"Invalid JSON value: {str(e)[:100]}... Converting to NULL")
        return None

def safe_string_format(value, max_length=255):
    """Safely format string fields, returning None for any errors."""
    if pd.isna(value) or value == '' or value is None:
        return None
    try:
        string_value = str(value)
        return string_value[:max_length] if len(string_value) > max_length else string_value
    except Exception as e:
        logger.warning(f"Invalid string value: {str(e)[:100]}... Converting to NULL")
        return None

def load_csv_data(file_path):
    """Load and preprocess CSV data."""
    try:
        # Read CSV file
        df = pd.read_csv(file_path, low_memory=False)
        
        # Verify column names match expected structure
        expected_columns = ['id', 'message_id', 'template_id', 'content_type', 
                          'text', 'media', 'cta', 'placeholders']
        
        # Ensure all expected columns exist, fill missing ones with None
        for col in expected_columns:
            if col not in df.columns:
                logger.warning(f"Missing column {col} in CSV, adding with NULL values")
                df[col] = None
        
        # Process JSON fields
        json_columns = ['media', 'cta', 'placeholders']
        for col in json_columns:
            df[col] = df[col].apply(safe_json_format)
        
        # Process string fields
        string_columns = ['id', 'message_id', 'template_id', 'content_type']
        for col in string_columns:
            df[col] = df[col].apply(safe_string_format)
        
        # Process text field
        df['text'] = df['text'].apply(lambda x: safe_string_format(x, max_length=None))
        
        return df[expected_columns]  # Ensure columns are in the correct order
    except Exception as e:
        logger.error(f"Failed to load CSV file: {e}")
        raise

def insert_data(conn, df):
    """Insert data into PostgreSQL table using batch operations."""
    try:
        # Convert DataFrame to list of tuples, replacing any remaining NaN with None
        data = []
        for row in df.itertuples(index=False):
            row_data = tuple(None if pd.isna(x) else x for x in row)
            data.append(row_data)
        
        # Insert data in batches
        batch_size = 5000
        
        insert_query = """
            INSERT INTO content_table (
                id, message_id, template_id, content_type,
                text, media, cta, placeholders
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        total_rows = 0
        with conn.cursor() as cur:
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                try:
                    execute_batch(cur, insert_query, batch, page_size=batch_size)
                    conn.commit()
                    total_rows += len(batch)
                    logger.info(f"Inserted batch of {len(batch)} rows. Total: {total_rows}")
                except Exception as e:
                    logger.error(f"Error inserting batch: {e}")
                    conn.rollback()
                    # Continue with next batch instead of failing completely
                    continue
            
        logger.info(f"Completed insertion. Total rows inserted: {total_rows}")
    except Exception as e:
        logger.error(f"Failed to insert data: {e}")
        conn.rollback()
        raise

def verify_data(conn):
    """Verify the data was loaded correctly."""
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM content_table')
            count = cur.fetchone()[0]
            
            cur.execute('SELECT * FROM content_table LIMIT 1')
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
    CSV_FILE_PATH = 'content_table.csv'
    main(CSV_FILE_PATH)
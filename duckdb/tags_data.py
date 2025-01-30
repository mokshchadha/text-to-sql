import duckdb
import random
import uuid
from datetime import datetime, timedelta
import numpy as np
from typing import List, Tuple

# DuckDB connection - this will create a new database file if it doesn't exist
DB_PATH = 'orders.duckdb'

try:
    # Connect to DuckDB with a larger memory limit
    conn = duckdb.connect(DB_PATH)
    conn.execute("SET memory_limit='32GB'")  # Adjust based on your system
    conn.execute("PRAGMA threads=8")  # Adjust based on your CPU cores
    print("Successfully connected to DuckDB!")

    # Create table
    conn.execute('''
        DROP TABLE IF EXISTS orders
    ''')

    conn.execute('''
        CREATE TABLE orders (
            orderNo VARCHAR,
            tags VARCHAR[],
            created_at TIMESTAMP,
            completed_at TIMESTAMP
        )
    ''')

    print("Table created successfully!")

    # Generate pool of 200 tags
    def generate_tag_pool(size=200):
        categories = ['priority', 'status', 'region', 'type', 'department']
        tags = []
        for category in categories:
            for i in range(size // len(categories)):
                tags.append(f"{category}_{i}")
        return tags

    tag_pool = generate_tag_pool()
    print(f"Generated {len(tag_pool)} unique tags")

    # Generate random datetime between two dates
    def random_datetime(size: int) -> List[datetime]:
        start_ts = datetime(2023, 1, 1).timestamp()
        end_ts = datetime(2024, 12, 31).timestamp()
        
        timestamps = np.random.uniform(start_ts, end_ts, size)
        return [datetime.fromtimestamp(ts) for ts in timestamps]

    def generate_completion_times(created_dates: List[datetime]) -> List[datetime]:
        completion_dates = []
        for created_at in created_dates:
            max_completion = min(
                datetime(2024, 12, 31),
                created_at + timedelta(days=30)
            )
            
            if max_completion <= created_at:
                completion_date = created_at + timedelta(seconds=random.randint(1, 3600))
            else:
                completion_ts = random.uniform(
                    (created_at + timedelta(seconds=1)).timestamp(),
                    max_completion.timestamp()
                )
                completion_date = datetime.fromtimestamp(completion_ts)
            
            completion_dates.append(completion_date)
        
        return completion_dates

    # Generate data in larger chunks
    def generate_batch(batch_size: int = 100000) -> List[Tuple]:
        # Generate order numbers
        order_nos = [str(uuid.uuid4()) for _ in range(batch_size)]
        
        # Generate tags (50 tags per order)
        tags = [random.sample(tag_pool, 50) for _ in range(batch_size)]
        
        # Generate timestamps
        created_dates = random_datetime(batch_size)
        completed_dates = generate_completion_times(created_dates)
        
        # Create list of tuples
        return list(zip(order_nos, tags, created_dates, completed_dates))

    # Insert data in larger batches with transaction control
    total_records = 50_000_000
    batch_size = 10000  # Increased batch size
    num_batches = total_records // batch_size

    try:
        records_inserted = 0
        
        # Begin transaction
        conn.execute('BEGIN TRANSACTION')
        
        for i in range(num_batches):
            batch_data = generate_batch(batch_size)
            
            # Insert batch using parameterized query
            conn.executemany(
                'INSERT INTO orders (orderNo, tags, created_at, completed_at) VALUES (?, ?, ?, ?)',
                batch_data
            )
            
            records_inserted += batch_size
            
            # Commit every 500k records
            if (i + 1) % 5 == 0:
                conn.execute('COMMIT')
                conn.execute('BEGIN TRANSACTION')
                percentage_complete = (records_inserted / total_records) * 100
                print(f"Inserted {records_inserted:,} records ({percentage_complete:.1f}% complete)")
        
        # Final commit
        conn.execute('COMMIT')

        # Verify final count
        count = conn.execute('SELECT count(*) FROM orders').fetchone()[0]
        print(f"\nTotal records inserted: {count:,}")

        # Display sample data
        print("\nSample records:")
        sample = conn.execute('''
            SELECT 
                orderNo,
                array_length(tags) as tag_count,
                created_at,
                completed_at,
                epoch_ms(completed_at - created_at)/1000 as completion_time_seconds
            FROM orders 
            LIMIT 5
        ''').fetchall()

        for record in sample:
            print(f"\nOrder: {record[0]}")
            print(f"Number of tags: {record[1]}")
            print(f"Created at: {record[2]}")
            print(f"Completed at: {record[3]}")
            print(f"Completion time (seconds): {record[4]}")

    except Exception as e:
        conn.execute('ROLLBACK')
        print(f"Error during data insertion: {e}")
        raise

except Exception as e:
    print(f"Error connecting to DuckDB: {e}")
    raise

finally:
    if 'conn' in locals():
        conn.close()
        print("\nConnection closed.")
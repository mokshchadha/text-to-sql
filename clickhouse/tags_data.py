from clickhouse_driver import Client
import random
import string
import uuid
from datetime import datetime, timedelta

# ClickHouse connection settings
CLICKHOUSE_HOST = 'localhost'
CLICKHOUSE_PORT = 9000
CLICKHOUSE_USER = 'admin'
CLICKHOUSE_PASSWORD = 'strongpassword'
CLICKHOUSE_DATABASE = 'wabaservicedb'

try:
    # Connect to ClickHouse with credentials
    client = Client(
        host=CLICKHOUSE_HOST,
        port=CLICKHOUSE_PORT,
        user=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD,
        database=CLICKHOUSE_DATABASE,
        settings={
            'use_numpy': False  # Disabled NumPy
        }
    )

    # Test connection
    client.execute('SELECT 1')
    print("Successfully connected to ClickHouse!")

    # Create table
    client.execute('''
        DROP TABLE IF EXISTS orders
    ''')

    client.execute('''
        CREATE TABLE orders (
            orderNo String,
            tags Array(String),
            created_at DateTime,
            completed_at DateTime
        ) ENGINE = MergeTree()
        ORDER BY orderNo
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
    def random_datetime(start_date, end_date):
        if start_date >= end_date:
            return start_date
        
        time_between = end_date - start_date
        days_between = max(0, time_between.days)
        random_days = random.randint(0, days_between)
        random_seconds = random.randint(0, 86399)
        return start_date + timedelta(days=random_days, seconds=random_seconds)

    # Start and end date range for created_at
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)

    def generate_batch(batch_size=10000):
        orders = []
        for _ in range(batch_size):
            # Generate order data
            order_no = str(uuid.uuid4())
            tags = random.sample(tag_pool, 50)
            
            created_at = random_datetime(start_date, end_date)
            completion_end_date = min(end_date, created_at + timedelta(days=30))
            
            if completion_end_date <= created_at:
                completed_at = created_at + timedelta(seconds=random.randint(1, 3600))
            else:
                completed_at = random_datetime(created_at + timedelta(seconds=1), completion_end_date)
            
            orders.append({
                'orderNo': order_no,
                'tags': tags,
                'created_at': created_at,
                'completed_at': completed_at
            })
        return orders

    # Insert data in batches
    total_records = 5_000_000
    batch_size = 10000
    num_batches = total_records // batch_size

    try:
        records_inserted = 0
        for i in range(num_batches):
            batch = generate_batch(batch_size)
            
            # Insert batch
            client.execute(
                'INSERT INTO orders (orderNo, tags, created_at, completed_at) VALUES',
                batch,
                types_check=True
            )
            
            records_inserted += len(batch)
            
            if (i + 1) % 10 == 0:
                percentage_complete = (records_inserted / total_records) * 100
                print(f"Inserted {records_inserted:,} records ({percentage_complete:.1f}% complete)")

        # Verify final count
        count = client.execute('SELECT count() FROM orders')[0][0]
        print(f"\nTotal records inserted: {count:,}")

        # Display sample data
        print("\nSample records:")
        sample = client.execute('''
            SELECT 
                orderNo,
                length(tags) as tag_count,
                created_at,
                completed_at,
                dateDiff('second', created_at, completed_at) as completion_time_seconds
            FROM orders 
            LIMIT 5
        ''')

        for record in sample:
            print(f"\nOrder: {record[0]}")
            print(f"Number of tags: {record[1]}")
            print(f"Created at: {record[2]}")
            print(f"Completed at: {record[3]}")
            print(f"Completion time (seconds): {record[4]}")

    except Exception as e:
        print(f"Error during data insertion: {e}")
        raise

except Exception as e:
    print(f"Error connecting to ClickHouse: {e}")
    raise

finally:
    if 'client' in locals():
        client.disconnect()
        print("\nConnection closed.")
from clickhouse_driver import Client
import time
from datetime import datetime, timedelta

# Connection settings
client = Client(
    host='localhost',
    port=9000,
    user='admin',
    password='strongpassword',
    database='wabaservicedb'
)

def measure_execution_time(query):
    start_time = time.time()
    result = client.execute(query)
    execution_time = time.time() - start_time
    return result, execution_time

# 1. Test Maximum Columns
def test_max_columns():
    try:
        # Create a table with 1000 columns (as a test)
        columns = ','.join([f'col_{i} String' for i in range(1000)])
        create_query = f'''
            CREATE TABLE test_max_columns (
                id UInt32,
                {columns}
            ) ENGINE = MergeTree()
            ORDER BY id
        '''
        client.execute('DROP TABLE IF EXISTS test_max_columns')
        client.execute(create_query)
        print("Successfully created table with 1000 columns")
    except Exception as e:
        print(f"Max columns test failed at: {e}")
    finally:
        client.execute('DROP TABLE IF EXISTS test_max_columns')

# 2. Test Filter Search Performance
def test_filter_performance():
    print("\n=== Filter Performance Tests ===")
    
    # Test with index
    query_with_index = "SELECT COUNT(*) FROM orders WHERE orderNo = '123456'"
    _, time_with_index = measure_execution_time(query_with_index)
    print(f"Query with index took: {time_with_index:.4f} seconds")
    
    # Test without index
    query_without_index = "SELECT COUNT(*) FROM orders WHERE created_at > '2023-06-01'"
    _, time_without_index = measure_execution_time(query_without_index)
    print(f"Query without index took: {time_without_index:.4f} seconds")

# 3. Test Large Data Loading
def test_large_data_loading():
    print("\n=== Large Data Loading Test ===")
    
    client.execute('''
        CREATE TABLE IF NOT EXISTS test_large (
            id UInt32,
            value1 String,
            value2 String,
            value3 Float64,
            value4 DateTime,
            value5 Array(String)
        ) ENGINE = MergeTree()
        ORDER BY id
    ''')
    
    # Generate test data
    start_time = time.time()
    batch_size = 10000
    data = []
    for i in range(batch_size):
        data.append({
            'id': i,
            'value1': f'string_{i}',
            'value2': f'text_{i}',
            'value3': float(i),
            'value4': datetime.now(),
            'value5': [f'tag_{j}' for j in range(5)]
        })
    
    # Insert data
    client.execute('INSERT INTO test_large VALUES', data)
    load_time = time.time() - start_time
    print(f"Loading {batch_size} records took: {load_time:.4f} seconds")
    
    client.execute('DROP TABLE test_large')

# 4. Test Aggregation Performance
def test_aggregation_performance():
    print("\n=== Aggregation Performance Tests ===")
    
    # Simple aggregation
    query_simple = "SELECT COUNT(*) FROM orders"
    _, time_simple = measure_execution_time(query_simple)
    print(f"Simple COUNT(*) took: {time_simple:.4f} seconds")
    
    # Complex aggregation
    query_complex = """
        SELECT 
            toYYYYMM(created_at) as month,
            COUNT(*) as count,
            COUNT(DISTINCT orderNo) as unique_orders
        FROM orders 
        GROUP BY month
        ORDER BY month
    """
    _, time_complex = measure_execution_time(query_complex)
    print(f"Complex aggregation took: {time_complex:.4f} seconds")

# 5. Test DISTINCT Performance
def test_array_search_performance():
    print("\n=== Array Search Performance Tests ===")
    
    # Single tag search
    single_tag_query = """
        SELECT COUNT(*)
        FROM orders
        WHERE has(tags, 'priority_1')
    """
    result, time_single = measure_execution_time(single_tag_query)
    print(f"Single tag search count: {result[0][0]}")
    print(f"Single tag search took: {time_single:.4f} seconds")
    
    # Multiple tags search (ANY)
    multi_tag_any_query = """
        SELECT COUNT(*)
        FROM orders
        WHERE hasAny(tags, ['priority_1', 'status_2', 'region_3'])
    """
    result, time_multi_any = measure_execution_time(multi_tag_any_query)
    print(f"Multiple tags (ANY) search count: {result[0][0]}")
    print(f"Multiple tags (ANY) search took: {time_multi_any:.4f} seconds")
    
    # Multiple tags search (ALL)
    multi_tag_all_query = """
        SELECT COUNT(*)
        FROM orders
        WHERE hasAll(tags, ['priority_1', 'status_2', 'region_3'])
    """
    result, time_multi_all = measure_execution_time(multi_tag_all_query)
    print(f"Multiple tags (ALL) search count: {result[0][0]}")
    print(f"Multiple tags (ALL) search took: {time_multi_all:.4f} seconds")
    
    # Complex tag search with additional conditions
    complex_tag_query = """
        SELECT 
            toYYYYMM(created_at) as month,
            COUNT(*) as orders_count
        FROM orders
        WHERE hasAny(tags, ['priority_1', 'status_2'])
            AND created_at >= '2023-06-01'
            AND created_at < '2024-01-01'
        GROUP BY month
        ORDER BY month
    """
    result, time_complex = measure_execution_time(complex_tag_query)
    print(f"Complex tag search took: {time_complex:.4f} seconds")
    
    # Array length analysis
    array_stats_query = """
        SELECT 
            min(length(tags)) as min_tags,
            max(length(tags)) as max_tags,
            avg(length(tags)) as avg_tags,
            count() as total_orders
        FROM orders
    """
    result, time_stats = measure_execution_time(array_stats_query)
    print("\nArray statistics:")
    print(f"Min tags per order: {result[0][0]}")
    print(f"Max tags per order: {result[0][1]}")
    print(f"Avg tags per order: {result[0][2]:.2f}")
    print(f"Total orders: {result[0][3]}")

def test_distinct_performance():
    print("\n=== DISTINCT Operation Tests ===")
    
    # Test DISTINCT on a single column
    query_distinct = "SELECT COUNT(DISTINCT arrayJoin(tags)) FROM orders"
    result, execution_time = measure_execution_time(query_distinct)
    print(f"DISTINCT tags count: {result[0][0]}")
    print(f"DISTINCT operation took: {execution_time:.4f} seconds")

# 6. Test Partitioning
def test_partitioning():
    print("\n=== Partitioning Test ===")
    
    # Create a partitioned table
    client.execute('''
        CREATE TABLE IF NOT EXISTS orders_partitioned (
            orderNo String,
            tags Array(String),
            created_at DateTime,
            completed_at DateTime
        ) ENGINE = MergeTree()
        PARTITION BY toYYYYMM(created_at)
        ORDER BY orderNo
    ''')
    
    # Get partition info
    partitions = client.execute("SELECT partition, name FROM system.parts WHERE table = 'orders_partitioned'")
    print(f"Number of partitions: {len(partitions)}")
    
    client.execute('DROP TABLE orders_partitioned')

# Run all tests
if __name__ == "__main__":
    print("Starting ClickHouse Performance Analysis...")
    
    test_max_columns()
    test_filter_performance()
    test_large_data_loading()
    test_aggregation_performance()
    test_array_search_performance()
    test_distinct_performance()
    # test_partitioning()
    
    print("\n=== Array Search Query Examples ===")
    print("""
    # Example queries for array searching:
    
    # 1. Basic tag search:
    SELECT * FROM orders WHERE has(tags, 'priority_1')
    
    # 2. Search for any of multiple tags:
    SELECT * FROM orders WHERE hasAny(tags, ['priority_1', 'status_2'])
    
    # 3. Search for all specified tags:
    SELECT * FROM orders WHERE hasAll(tags, ['priority_1', 'status_2'])
    
    # 4. Complex tag search with aggregation:
    SELECT 
        toYYYYMM(created_at) as month,
        COUNT(*) as orders_count
    FROM orders
    WHERE hasAny(tags, ['priority_1', 'status_2'])
        AND created_at >= '2023-06-01'
    GROUP BY month
    ORDER BY month
    
    # 5. Search with array size condition:
    SELECT * FROM orders 
    WHERE length(tags) > 45 
        AND has(tags, 'priority_1')
    
    # 6. Tag frequency analysis:
    SELECT 
        tag,
        COUNT(*) as usage_count
    FROM orders
    ARRAY JOIN tags as tag
    GROUP BY tag
    ORDER BY usage_count DESC
    LIMIT 10
    """)
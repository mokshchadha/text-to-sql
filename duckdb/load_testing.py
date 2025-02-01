import duckdb
import time
from datetime import datetime, timedelta

# Connection settings
DB_PATH = 'orders.duckdb'

def measure_execution_time(conn, query):
    start_time = time.time()
    result = conn.execute(query).fetchall()
    execution_time = time.time() - start_time
    return result, execution_time

# 1. Test Maximum Columns
def test_max_columns(conn):
    try:
        # Create a table with 1000 columns (as a test)
        columns = ','.join([f'col_{i} VARCHAR' for i in range(1000)])
        create_query = f'''
            CREATE TABLE test_max_columns (
                id INTEGER,
                {columns}
            )
        '''
        conn.execute('DROP TABLE IF EXISTS test_max_columns')
        conn.execute(create_query)
        print("Successfully created table with 1000 columns")
    except Exception as e:
        print(f"Max columns test failed at: {e}")
    finally:
        conn.execute('DROP TABLE IF EXISTS test_max_columns')

# 2. Test Filter Search Performance
def test_filter_performance(conn):
    print("\n=== Filter Performance Tests ===")
    
    # Test with index
    query_with_index = "SELECT COUNT(*) FROM orders WHERE orderNo = '123456'"
    _, time_with_index = measure_execution_time(conn, query_with_index)
    print(f"Query with index took: {time_with_index:.4f} seconds")
    
    # Test without index
    query_without_index = "SELECT COUNT(*) FROM orders WHERE created_at > '2023-06-01'"
    _, time_without_index = measure_execution_time(conn, query_without_index)
    print(f"Query without index took: {time_without_index:.4f} seconds")

# 3. Test Large Data Loading
def test_large_data_loading(conn):
    print("\n=== Large Data Loading Test ===")
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS test_large (
            id INTEGER,
            value1 VARCHAR,
            value2 VARCHAR,
            value3 DOUBLE,
            value4 TIMESTAMP,
            value5 VARCHAR[]
        )
    ''')
    
    # Generate test data
    start_time = time.time()
    batch_size = 10000
    data = []
    for i in range(batch_size):
        data.append((
            i,
            f'string_{i}',
            f'text_{i}',
            float(i),
            datetime.now(),
            [f'tag_{j}' for j in range(5)]
        ))
    
    # Insert data
    conn.executemany(
        'INSERT INTO test_large VALUES (?, ?, ?, ?, ?, ?)',
        data
    )
    load_time = time.time() - start_time
    print(f"Loading {batch_size} records took: {load_time:.4f} seconds")
    
    conn.execute('DROP TABLE test_large')

# 4. Test Aggregation Performance
def test_aggregation_performance(conn):
    print("\n=== Aggregation Performance Tests ===")
    
    # Simple aggregation
    query_simple = "SELECT COUNT(*) FROM orders"
    _, time_simple = measure_execution_time(conn, query_simple)
    print(f"Simple COUNT(*) took: {time_simple:.4f} seconds")
    
    # Complex aggregation
    query_complex = """
        SELECT 
            strftime(created_at, '%Y%m') as month,
            COUNT(*) as count,
            COUNT(DISTINCT orderNo) as unique_orders
        FROM orders 
        GROUP BY month
        ORDER BY month
    """
    _, time_complex = measure_execution_time(conn, query_complex)
    print(f"Complex aggregation took: {time_complex:.4f} seconds")

# 5. Test Array Search Performance
def test_array_search_performance(conn):
    print("\n=== Array Search Performance Tests ===")
    
    # Single tag search
    single_tag_query = """
        SELECT COUNT(*)
        FROM orders
        WHERE list_contains(tags, 'priority_1')
    """
    result, time_single = measure_execution_time(conn, single_tag_query)
    print(f"Single tag search count: {result[0][0]}")
    print(f"Single tag search took: {time_single:.4f} seconds")
    
    # Multiple tags search (ANY)
    multi_tag_any_query = """
        SELECT COUNT(*)
        FROM orders
        WHERE array_length(array_intersect(tags, ['priority_1', 'status_2', 'region_3'])) > 0
    """
    result, time_multi_any = measure_execution_time(conn, multi_tag_any_query)
    print(f"Multiple tags (ANY) search count: {result[0][0]}")
    print(f"Multiple tags (ANY) search took: {time_multi_any:.4f} seconds")
    
    # Multiple tags search (ALL)
    multi_tag_all_query = """
        SELECT COUNT(*)
        FROM orders
        WHERE array_length(array_intersect(tags, ['priority_1', 'status_2', 'region_3'])) = 3
    """
    result, time_multi_all = measure_execution_time(conn, multi_tag_all_query)
    print(f"Multiple tags (ALL) search count: {result[0][0]}")
    print(f"Multiple tags (ALL) search took: {time_multi_all:.4f} seconds")
    
    # Complex tag search with additional conditions
    complex_tag_query = """
        SELECT 
            strftime(created_at, '%Y%m') as month,
            COUNT(*) as orders_count
        FROM orders
        WHERE array_length(array_intersect(tags, ['priority_1', 'status_2'])) > 0
            AND created_at >= '2023-06-01'
            AND created_at < '2024-01-01'
        GROUP BY month
        ORDER BY month
    """
    result, time_complex = measure_execution_time(conn, complex_tag_query)
    print(f"Complex tag search took: {time_complex:.4f} seconds")
    
    # Array length analysis
    array_stats_query = """
        SELECT 
            min(array_length(tags)) as min_tags,
            max(array_length(tags)) as max_tags,
            avg(array_length(tags))::FLOAT as avg_tags,
            count(*) as total_orders
        FROM orders
    """
    result, time_stats = measure_execution_time(conn, array_stats_query)
    print("\nArray statistics:")
    print(f"Min tags per order: {result[0][0]}")
    print(f"Max tags per order: {result[0][1]}")
    print(f"Avg tags per order: {result[0][2]:.2f}")
    print(f"Total orders: {result[0][3]}")

def test_distinct_performance(conn):
    print("\n=== DISTINCT Operation Tests ===")
    
    # Test DISTINCT on a single column
    query_distinct = """
        WITH RECURSIVE unnested AS (
            SELECT UNNEST(tags) as tag FROM orders
        )
        SELECT COUNT(DISTINCT tag) FROM unnested
    """
    result, execution_time = measure_execution_time(conn, query_distinct)
    print(f"DISTINCT tags count: {result[0][0]}")
    print(f"DISTINCT operation took: {execution_time:.4f} seconds")

def calculate_p90_execution_time(conn, query, iterations=100):
    """
    Calculate P90 execution time for a given query
    
    Parameters:
    conn: DuckDB connection
    query: Query to test
    iterations: Number of times to run the query (default 100)
    
    Returns:
    tuple: (p90_time, execution_times, stats_dict)
    """
    execution_times = []
    print(f"\nRunning query {iterations} times to calculate P90...")
    
    try:
        for i in range(iterations):
            start_time = time.time()
            conn.execute(query).fetchall()
            execution_time = time.time() - start_time
            execution_times.append(execution_time)
            
            # Print progress every 10 iterations
            if (i + 1) % 10 == 0:
                print(f"Completed {i + 1}/{iterations} iterations")
        
        # Calculate P90 and other statistics using DuckDB
        times_query = f"""
        WITH times AS (
            SELECT UNNEST({execution_times}) as exec_time
        )
        SELECT 
            QUANTILE(exec_time, 0.9) as p90,
            MIN(exec_time) as min_time,
            MAX(exec_time) as max_time,
            AVG(exec_time) as mean_time,
            STDDEV(exec_time) as std_dev
        FROM times
        """
        stats = conn.execute(times_query).fetchone()
        
        stats_dict = {
            'p90': stats[0],
            'min_time': stats[1],
            'max_time': stats[2],
            'mean_time': stats[3],
            'std_dev': stats[4]
        }
        
        return stats[0], execution_times, stats_dict
        
    except Exception as e:
        print(f"Error calculating P90: {e}")
        return None, None, None

def test_p90_performance(conn):
    """Test P90 performance for different query types"""
    print("\n=== P90 Performance Tests ===")
    
    test_queries = {
        "Simple Count": "SELECT COUNT(*) FROM orders",
        "Filtered Count": "SELECT COUNT(*) FROM orders WHERE created_at > '2023-06-01'",
        "Array Search": """
            SELECT COUNT(*)
            FROM orders
            WHERE list_contains(tags, 'priority_1')
        """,
        "Complex Aggregation": """
            SELECT 
                strftime(created_at, '%Y%m') as month,
                COUNT(*) as count
            FROM orders 
            WHERE array_length(array_intersect(tags, ['priority_1', 'status_2'])) > 0
            GROUP BY month
            ORDER BY month
        """
    }
    
    results = {}
    for query_name, query in test_queries.items():
        print(f"\nTesting P90 for: {query_name}")
        p90_time, _, stats = calculate_p90_execution_time(conn, query, iterations=500)
        
        if p90_time and stats:
            print(f"""
Performance Statistics for {query_name}:
- P90 Time:          {stats['p90']:.4f} seconds
- Minimum Time:      {stats['min_time']:.4f} seconds
- Maximum Time:      {stats['max_time']:.4f} seconds
- Mean Time:         {stats['mean_time']:.4f} seconds
- Standard Deviation: {stats['std_dev']:.4f} seconds
            """)
            results[query_name] = stats

    return results


def run_all_tests():
    try:
        print("Starting DuckDB Performance Analysis...")
        conn = duckdb.connect(DB_PATH)
        
        # Configure DuckDB settings for better performance
        conn.execute("SET memory_limit='32GB'")  # Adjust based on your system
        conn.execute("PRAGMA threads=8")  # Adjust based on your CPU cores
        
        test_max_columns(conn)
        test_filter_performance(conn)
        test_large_data_loading(conn)
        test_aggregation_performance(conn)
        test_array_search_performance(conn)
        test_distinct_performance(conn)
        p90_results = test_p90_performance(conn)
        
        print("\n=== P90 Performance Summary ===")
        for query_name, stats in p90_results.items():
            print(f"{query_name}: P90 = {stats['p90']:.4f} seconds")
        
        print("\n=== Array Search Query Examples ===")
        print("""
        # Example queries for array searching in DuckDB:
        
        # 1. Basic tag search:
        SELECT * FROM orders WHERE list_contains(tags, 'priority_1')
        
        # 2. Search for any of multiple tags:
        SELECT * FROM orders 
        WHERE array_length(array_intersect(tags, ['priority_1', 'status_2'])) > 0
        
        # 3. Search for all specified tags:
        SELECT * FROM orders 
        WHERE array_length(array_intersect(tags, ['priority_1', 'status_2'])) = 2
        
        # 4. Complex tag search with aggregation:
        SELECT 
            strftime(created_at, '%Y%m') as month,
            COUNT(*) as orders_count
        FROM orders
        WHERE array_length(array_intersect(tags, ['priority_1', 'status_2'])) > 0
            AND created_at >= '2023-06-01'
        GROUP BY month
        ORDER BY month
        
        # 5. Search with array size condition:
        SELECT * FROM orders 
        WHERE array_length(tags) > 45 
            AND list_contains(tags, 'priority_1')
        
        # 6. Tag frequency analysis:
        WITH RECURSIVE tag_counts AS (
            SELECT UNNEST(tags) as tag
            FROM orders
        )
        SELECT 
            tag,
            COUNT(*) as usage_count
        FROM tag_counts
        GROUP BY tag
        ORDER BY usage_count DESC
        LIMIT 10
        """)
        
    except Exception as e:
        print(f"Error during testing: {e}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()
            print("\nConnection closed.")

if __name__ == "__main__":
    run_all_tests()
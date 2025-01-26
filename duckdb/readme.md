=== duck db insertion and size of 5 million records ===
Created at: 2023-08-20 19:01:43.091603
Completed at: 2023-09-10 23:06:12.447900
Completion time (seconds): 1829069.356

=== Filter Performance Tests ===
Query with index took: 0.0761 seconds
Query without index took: 0.0182 seconds

=== Large Data Loading Test ===
Loading 10000 records took: 4.4915 seconds

=== Aggregation Performance Tests ===
Simple COUNT(*) took: 0.0007 seconds
Complex aggregation took: 0.4973 seconds

=== Array Search Performance Tests ===
Single tag search count: 1250035
Single tag search took: 0.8846 seconds
Multiple tags (ANY) search count: 2902234
Multiple tags (ANY) search took: 19.8607 seconds
Multiple tags (ALL) search count: 74873
Multiple tags (ALL) search took: 24.5050 seconds
Complex tag search took: 6.1939 seconds

Array statistics:
Min tags per order: 50
Max tags per order: 50
Avg tags per order: 50.00
Total orders: 5000000

=== DISTINCT Operation Tests ===
DISTINCT tags count: 200
DISTINCT operation took: 2.6855 seconds

=== Array Search Query Examples ===

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
        
=== Apache Flink === 
DuckDB doesn't have direct Apache Flink support like ClickHouse does.
There are other ways like python data stream
DuckDB-Wasm with Arrow Streaming
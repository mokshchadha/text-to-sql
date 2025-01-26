===- Max number of columns allowed === 
Default limit is 1000 columns
Can be configured up to several thousand columns using the max_columns_to_read setting
Best practice is to keep it under 1000 for optimal performance
Recommendation: If you need more columns, consider normalizing your data model

=== Filter Performance Tests ===
Query with index took: 0.0774 seconds
Query without index took: 0.0924 seconds

=== Large Data Loading Test ===
Loading 10000 records took: 0.0894 seconds

=== Aggregation Performance Tests === (5 million records)
Simple COUNT(*) took: 0.0069 seconds
Complex aggregation took: 2.2557 seconds

=== DISTINCT Operation Tests === (5million - SELECT COUNT(DISTINCT arrayJoin(tags)) FROM order)
DISTINCT tags count: 200
DISTINCT operation took: 3.3794 seconds

=== Partitioning Test ===
Yes possible 

=== Flink Support === 
Yes, ClickHouse integrates well with Apache Flink
Official Flink ClickHouse Connector is available 

=== Array Search Query Examples ===

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

=== time to insert / size 5 million records ==== 
Created at: 2024-06-02 14:58:50
Completed at: 2024-06-10 14:04:27
Completion time (seconds): 687937
Size -- 996 mb
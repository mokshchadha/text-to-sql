from elasticsearch import Elasticsearch
import time

# Connect to Elasticsearch
es = Elasticsearch(["http://localhost:9200"])
index_name = "bulk_insert_index"

# Query to fetch a document by ID
def fetch_document(doc_id):
    start_time = time.time()
    response = es.get(index=index_name, id=doc_id)
    end_time = time.time()

    print("Document fetched:", response["_source"])
    print(f"Time taken: {end_time - start_time:.6f} seconds")

# Example: Fetch document with ID 1
fetch_document(1)

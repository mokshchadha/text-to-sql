from elasticsearch import Elasticsearch, helpers
import random
import string

es = Elasticsearch(["http://localhost:9200"])
index_name = "bulk_insert_index"

def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_document():
    return {f"key_{i}": random_string(20) for i in range(500)}

def generate_bulk_data():
    for i in range(100000):
        yield {
            "_index": index_name,
            "_id": i,
            "_source": generate_document()
        }

if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)

helpers.bulk(es, generate_bulk_data())

print("100,000 documents inserted successfully!")

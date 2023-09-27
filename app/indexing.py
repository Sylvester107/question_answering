from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
import pandas as pd

df=pd.read_csv('app\pairings\passage_metadata_emb.csv')

#es = Elasticsearch(
 #   [{'host': 'localhost', 'port': 9200,'scheme':'http'}],
  #  verify_certs=False,  # Set to True if valid SSL certificates exists
   # request_timeout=30  #  the timeout as needed
#)

#connect to elasticsearch client
es = Elasticsearch(
  "https://92d997736474439dae5ccfaedc2ad990.us-central1.gcp.cloud.es.io:443",
  api_key="R2xyODFZb0I4TjlWWlhYRWNGZkM6UzNwM20wWVZRdDJQUktLelEyMGdDUQ=="
)

#create an index
#es.indices.create(index='my_index')

# Create a function to prepare documents
documents = []

for _, row in df.iterrows():
    document = {
        "passage": row["Passages"],
        "metadata": row["Metadata"],
        "embeddings": row["Embedding"]
    }
    documents.append(document)
from elasticsearch.helpers import bulk

index_name = "search-passagemetadataemb"  
def generate_actions():
    for doc in documents:
        yield {
            "_index": index_name,
            "_source": doc
        }

# Use the bulk helper function to efficiently index the documents
success, failed = bulk(es, generate_actions())

# Check for successful indexing
if failed:
    print(f"Failed to index {len(failed)} documents.")
else:
    print(f"Successfully indexed {len(success)} documents.")


# Use Pandas' apply function to efficiently prepare documents
#documents = df.apply(prepare_document, axis=1)

# Use Elasticsearch's streaming_bulk to efficiently index the documents
#es.bulk(operations=documents, pipeline="ent-search-generic-ingestion")

# Check for successful indexing
#if failed:
#    print(f"Failed to index {len(failed)} documents.")
#else:
 #   print(f"Successfully indexed {len(success)} documents.")

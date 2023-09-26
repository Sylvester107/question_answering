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
    #'https://f69b4906a1a446de9326cd49d8eda261.us-central1.gcp.cloud.es.io',
    api_key=('Sylvester Ampomah','Y3d6UTBvb0Jxd25Bb2xJQ3dPNUo6OEttM29ESjNRTzZxYXNETGJKRzRvUQ=='),
    #cloud_id="4e692d4fa9a94d7bacb913393827e0be:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJGY2OWI0OTA2YTFhNDQ2ZGU5MzI2Y2Q0OWQ4ZWRhMjYxJDc4NzgwNTVjNDJlNDRhNTE5YWUzNTA5MThmNWNiOGM0",
    #basic_auth=('yhungsly87@gmail.com','HEMVeY3d9y4a$jd')
)

#create an index
es.indices.create(index='my_index')

# Create a function to prepare documents
def prepare_document(row):
    return {
        "_index": "QA_index",
        "_source": {
            "passage": row['passage'],
            "metadata": row['metadata'],
            "embeddings": row['embeddings']
        }
    }

# Use Pandas' apply function to efficiently prepare documents
documents = df.apply(prepare_document, axis=1)

# Use Elasticsearch's streaming_bulk to efficiently index the documents
success, failed = streaming_bulk(es, documents, chunk_size=1000)

# Check for successful indexing
if failed:
    print(f"Failed to index {len(failed)} documents.")
else:
    print(f"Successfully indexed {len(success)} documents.")

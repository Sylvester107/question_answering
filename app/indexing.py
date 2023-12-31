from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
import pandas as pd
import numpy as np
df=pd.read_csv('app\pairings\passage_metadata_emb.csv')

#Convert embeddings to np array
df['Embedding'] = df['Embedding'].apply(lambda x: np.fromstring(x.replace('\n', '')[1:-1], sep=' '))


#if you are using a local intance of elasticsearch and kibana use this
#es = Elasticsearch(
 #   [{'host': 'localhost', 'port': 9200,'scheme':'http'}],
  #  verify_certs=False,  # Set to True if valid SSL certificates exists
   # request_timeout=30  #  the timeout as needed
#)

#connect to elasticsearch cloud client
es = Elasticsearch(
  "https://86781d93f79a4d2da8e59e9d57d0677f.us-central1.gcp.cloud.es.io:443",
  api_key="eE1XdlVZc0J2ck9TR0dVUVEzQmo6QUhJcmxiTWNRcm15dzNNUmhUQVRrdw=="
)



# Generate a list of dictionaries containing the passage, corresponding metadata and embeddings
def prepare_documents(df):
    documents = []

    for _, row in df.iterrows():
        #row["Embedding"].tolist()
        document = {
            "Passages": row["Passages"],
            "Metadata": row["Metadata"],
            "Embedding": {
                "type": "dense_vector",
                "dims": 3,  # Specify the dimensionality of your dense vectors
                "value": row["Embedding"].tolist()
        }}
        documents.append(document)
    return documents

documents=prepare_documents(df=df)
# Create a function to prepare documents for indexing
index_name = "search-questionanswering"  #index name created on elasticsearch
#index 
for doc_id, document in enumerate(documents):
    es.index(index=index_name, body=document, id=doc_id)

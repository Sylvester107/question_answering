from elasticsearch import Elasticsearch
import pandas as pd
from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer
import numpy as np

# Create a SentenceTransformerLoader instance (loads the model if not loaded already)
#model_loader = SentenceTransformerLoader()

# Get the loaded model
model = SentenceTransformer('sentence-transformers/multi-qa-distilbert-cos-v1')

# Define the question and compute its embeddings
question = "What is an offer"
question_embedding = model.encode(question)
question_embedding=question_embedding.tolist()
# Create an Elasticsearch client
es = Elasticsearch(
  "https://92d997736474439dae5ccfaedc2ad990.us-central1.gcp.cloud.es.io:443",
  api_key="Ym16RzI0b0JIcXpRTU9NQUNUNE46YnBmaUtCWHdTNXlnN1dZR2w4Rllqdw=="
)

index_name="search-passagemetadataemb"  #index name created on elasticsearch

  

    
response = es.search(
        index=index_name,
        q=question,
        size=3
    )


# Extract relevant passages, metadata, and scores
relevant_passages = []
for hit in response["hits"]["hits"]:
    passage = hit["_source"]["Passages"]
    metadata = hit["_source"]["Metadata"]
    score_1=hit['_score']
    passage_embedding = np.array(hit["_source"]["Embedding"]['value'])
    score = 1 - cosine(question_embedding, passage_embedding)  # Calculate cosine similarity
    relevant_passages.append({"passage": passage, "metadata": metadata, "score": score})

#Sort the relevant passages by score in descending order
relevant_passages.sort(key=lambda x: x["score"], reverse=True)

 #Get the top 3 relevant passages and their metadata
top_3_relevant_passages = relevant_passages[:3]

# Print or return the relevant passages and scores
for passage_info in top_3_relevant_passages:
    print("Passage:", passage_info["passage"])
    print("Metadata:", passage_info["metadata"])
    print("Score:", passage_info["score"])
print('\n')
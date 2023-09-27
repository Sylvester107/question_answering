from elasticsearch import Elasticsearch
import pandas as pd
from scipy.spatial.distance import cosine
from sentence_transformer_loader import SentenceTransformerLoader
import numpy as np

# Create a SentenceTransformerLoader instance (loads the model if not loaded already)
model_loader = SentenceTransformerLoader()

# Get the loaded model
model = model_loader.get_model()

# Create an Elasticsearch client
es = Elasticsearch(
  "https://92d997736474439dae5ccfaedc2ad990.us-central1.gcp.cloud.es.io:443",
  api_key="R2xyODFZb0I4TjlWWlhYRWNGZkM6UzNwM20wWVZRdDJQUktLelEyMGdDUQ=="
)

index_name="search-passagemetadataemb"  #index name created on elasticsearch

# Define the question and compute its embeddings
question = "What is an offer"
question_embedding = model.encode(question)  

# Define the Elasticsearch query using cosine similarity
query = {
    "size": 3,  # Number of relevant passages to retrieve
    "query": {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.queryVector, 'embeddings') + 1.0",
                "params": {"queryVector": question_embedding.tolist()}
            }
        }
    },
    "_source": ["passage", "metadata", "embeddings"]
}

# Execute the Elasticsearch search
results = es.search(index=index_name, body=query)

# Extract relevant passages, metadata, and scores
relevant_passages = []
for hit in results["hits"]["hits"]:
    passage = hit["_source"]["passage"]
    metadata = hit["_source"]["metadata"]
    passage_embedding = np.array(hit["_source"]["embeddings"])
    score = 1 - cosine(question_embedding, passage_embedding)  # Calculate cosine similarity
    relevant_passages.append({"passage": passage, "metadata": metadata, "score": score})

# Sort the relevant passages by score in descending order
relevant_passages.sort(key=lambda x: x["score"], reverse=True)

# Get the top 3 relevant passages and their metadata
top_3_relevant_passages = relevant_passages[:3]

# Print or return the relevant passages and scores
for passage_info in top_3_relevant_passages:
    print("Passage:", passage_info["passage"])
    print("Metadata:", passage_info["metadata"])
    print("Score:", passage_info["score"])
    print("\n")
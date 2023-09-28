from elasticsearch import Elasticsearch
import pandas as pd
from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer
import numpy as np
"""
function 1
"""
# returns a dataframe for the current query
def create_df(top_3_relevant_passages,question):
    QA_dict={}
    index=0
    for passage_info in top_3_relevant_passages:
        QA_dict[f"Passage {index}:"]=passage_info["passage"]
        QA_dict[f"Metadata {index}:"]= passage_info["metadata"]
        QA_dict[f"Score {index}:"]= passage_info["score"]
        QA_dict['Question']=question
        index=index+1
    
    df=pd.DataFrame([QA_dict])
    return df

"""
Function 2
"""
# Extract relevant passages, metadata, and scores
def Extraction(response):
    relevant_passages = []
    for hit in response["hits"]["hits"]:
        passage = hit["_source"]["Passages"]
        metadata = hit["_source"]["Metadata"]
        #score_1=hit['_score']
        passage_embedding = np.array(hit["_source"]["Embedding"]['value'])
        score = 1 - cosine(question_embedding, passage_embedding)  # Calculate cosine similarity
        relevant_passages.append({"passage": passage, "metadata": metadata, "score": score})

    #Sort the relevant passages by score in descending order
    relevant_passages.sort(key=lambda x: x["score"], reverse=True)
    #Get the top 3 relevant passages and their metadata
    top_3_relevant_passages = relevant_passages[:3]
    return top_3_relevant_passages

"""
Begin Retrieval
"""
#This dataframe will hold the result to all queries
result_df=pd.DataFrame()

# Get the loaded model
model = SentenceTransformer('sentence-transformers/multi-qa-distilbert-cos-v1')
breaker='y'
while breaker=='y':
    # Define the question and compute its embeddings
    question = input("Ask a question: ")
    question_embedding = model.encode(question)
    question_embedding=question_embedding.tolist()

    # Create an Elasticsearch client
    es = Elasticsearch(
    "https://92d997736474439dae5ccfaedc2ad990.us-central1.gcp.cloud.es.io:443",
    api_key="Ym16RzI0b0JIcXpRTU9NQUNUNE46YnBmaUtCWHdTNXlnN1dZR2w4Rllqdw=="
    )
   
    #index name created on elasticsearch
    index_name="search-passagemetadataemb" 
    #search
    response = es.search(
            index=index_name,
            q=question,
            size=3
        )
    top_3=Extraction(response=response)
    current_df=create_df(top_3,question=question)
    result_df = pd.concat([result_df, current_df], ignore_index=True)
    breaker=input('Do you have another question y/n: ').lower()


 


#Generate CSV file
filepath = "app\pairings\questions_answers.csv"
result_df.to_csv(filepath, index=False)


from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from elasticsearch import Elasticsearch
from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer
import logging


#Creat the flask instance Using create_app
app=Flask(__name__)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)
"""
Functions for request/response validation
"""
# Define a function for request validation
def validate_request(request_data):
    # Example: Validate that 'question' is present in the request
    if 'question' not in request_data:
        return False
    return True

# Define a function for response validation
def validate_response(response_data):
    # Example: Validate that 'message' is present in the response
    if 'message' not in response_data:
        return False
    return True

"""
Function for preparing csv for indexing
"""
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
"""
function for working with retrival responses
"""
# Extract relevant passages, metadata, and scores
def Extraction(response,question_embedding):
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

#create the elastic search instance
es = Elasticsearch(
  "https://86781d93f79a4d2da8e59e9d57d0677f.us-central1.gcp.cloud.es.io:443",
  api_key="eE1XdlVZc0J2ck9TR0dVUVEzQmo6QUhJcmxiTWNRcm15dzNNUmhUQVRrdw=="
)
app.logger.info(msg='es instance created')
"""
Question asking endpoint

"""
# Define an endpoint for receiving a user question via POST request
@app.route('/ask', methods=['POST'])
def receive_question():
    model = SentenceTransformer('sentence-transformers/multi-qa-distilbert-cos-v1')
    # Get the question from the request JSON data
    question_data = request.get_json()
    user_question = question_data.get('question')
    
    # Validate request data
    if not validate_request(question_data):
        app.logger.error(msg='Invalid request data')
        return jsonify({'error': 'Invalid request data'}), 400
    
    #return response
    question = user_question
    question_embedding = model.encode(question)
    question_embedding=question_embedding.tolist()
    #index name created on elasticsearch
    index_name="search-passagemetadataemb" 
    #search
    response = es.search(
            index=index_name,
            q=question,
            size=3
        )
    top_3=Extraction(response=response,question_embedding=question_embedding)
    results={}
    id=0 #  id for different passages 
    for passage_info in top_3:
        results[f"Passage {id}:"]=passage_info["passage"]
        results[f"Metadata {id}:"]= passage_info["metadata"]
        results[f"Score {id}:"]= passage_info["score"]
        id=id+1

    # Respond with a confirmation message
    response = {'message': 'Question received successfully',
                'qustion': user_question,
                'results': results
                }
    # Validate request data
    if not validate_response(response):
        return jsonify({'error': 'Invalid response data'}), 500
    return jsonify(response)


"""
File Upload endpoint
"""
@app.route('/upload_csv', methods=['POST'])
def upload_document():
    # Get the uploaded file from the request
    uploaded_file = request.files['file']
    
    if uploaded_file:
        app.logger.info(msg='file uploaded')
        # Process the uploaded file 
        
        file_path = 'uploads/' + uploaded_file.filename
        uploaded_file.save(file_path)
        df=pd.read_csv(file_path)

        #Convert embeddings to np array
        df['Embedding'] = df['Embedding'].apply(lambda x: np.fromstring(x.replace('\n', '')[1:-1], sep=' '))
        # Index the document in Elasticsearch
        documents=prepare_documents(df)
        

        # Create a function to prepare documents for indexing
        index_name = "search-passagemetadataemb"  #index name created on elasticsearch
        #index 
        for doc_id, document in enumerate(documents):
            es.index(index=index_name, body=document, id=doc_id)


        return jsonify({'message': 'Document uploaded and indexed successfully'})

    return jsonify({'message': 'No file uploaded'})

if __name__=='__main__':
    app.run()

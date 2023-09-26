
import pandas as pd
from sentence_transformers import SentenceTransformer

#Read the passage_metadata.csv file into a pandas dataframe
df=pd.read_csv('app\pairings\passage_metadata.csv')
#check to verify content
df.head()
# Using list comprehension create a list of strings to be passed to SentenceTransformer
List_of_strings=[string for string in df['Passages']]

#initiate a sentence transformer instance this will download the sentence transformer into your env
model = SentenceTransformer('multi-qa-distilbert-cos-v1')

#encode the sentences 
embeddings = model.encode(List_of_strings)

#the encoded sentences returns a numpy.ndarray convert to a list

list_embeddings=list(embeddings)
#insert the corresponding embeddings into the dataframe
df['Embedding']=list_embeddings
#verify
df.head()
#Create the CSV file passage_metadata_emb.csv
df.to_csv('/content/drive/MyDrive/pairings/passage_metadata_emb.csv')
print(f"CSV file passage_metadata_emb.csv has been created.")
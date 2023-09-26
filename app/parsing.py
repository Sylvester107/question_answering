''' this is a python file 
    you can use the jupyter interactive window(Use ctrl + shift + p) in vs code 
    to view the code line by line. A notebook would have been better for this tax.
'''
#import libraries
import pandas as pd
import numpy as np
import json
from pathlib import Path
import glob
import os

#inspect the one dataset
file_path='Data\Corpus\kwame-legal-EL-1680770407105_Technical.txt'
#open file in read mode
with open(file_path,'rt',encoding='UTF-8') as file:
    #read file contents into a variable
    file_contents=file.read()

#print the contents
# print(file_contents) #uncomment to print file contents to screen

#Findings after inspection
"""
_Technical.txt contains __section__ which is the Judgement
under each section is __paragraph__ 
"""
# Specify the folder path
folder_path = "Data\Corpus"

# Use glob to select text files and their corresponding metadata JSON files
file_pattern = os.path.join(folder_path, "*.txt")

#to store processed passages and corresponding metadata
all_passages=[]
all_metadata=[]
#initiate a for loop to iterate over files in corpus
for text_file_path in glob.glob(file_pattern):

    ## Extract the passages within paragraphs

    with open(text_file_path,'rt',encoding='UTF-8') as file:
        #read file contents into a variable
        file_contents_ls=file.readlines() #returnts a list

        #remove the newline character using list comprehension
        file_contents_ls=lines = [line.strip() for line in file_contents_ls]
    #print(file_contents_ls)


    #define a drop list
    drop_list=['__section__','__paragraph__']

    filtered_list=filtered_list = [item for item in file_contents_ls if item not in drop_list]
    #print to see output

    #print(filtered_list)

    
    #form 5 sentence each to form a passage


    # Define the number of consecutive strings to combine
    group_size = 5

    # Initialize an empty list to store the combined passages
    passages = []

    #for loop with a step to efficiently combine strings
    for i in range(0, len(filtered_list), group_size):
        passage = ' '.join(filtered_list[i:i + group_size])
        passages.append(passage)

    #combined passages Uncomment to check output 
    #for passage in passages:
        #print(passage)

    #join to form 1 passage
    processed_passage=' '.join(passages)
    all_passages.append(processed_passage)
    #print(passage_1)

    ##Extract metadata
    metadata_file_path = text_file_path.replace("Technical", "Metadata").replace(".txt", ".json")
    with open(metadata_file_path,'r',encoding='UTF-8') as f:
        #read file contents into a variable
        metadata=json.load(f)
    #print(metadata)

    all_metadata.append(metadata)

#Create a CSV file
passage_metadata={
    'Passages':all_passages,
    'Metadata':all_metadata
}
print(f'{all_passages[4]}\n\n\n,{all_metadata[4]}')
#filepath = "app\pairings\passage_metadata.csv"
#df=pd.DataFrame(passage_metadata)
#df.to_csv(filepath, index=False)

#print(f"CSV file '{filepath}' has been created.")

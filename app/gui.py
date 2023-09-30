import streamlit as st
import requests
import json
#Set the page configs
st.set_page_config(page_title='Question Answering bot',page_icon='😎',layout='centered')

#set the title
st.title("Question Answering System")
with st.form(key='question'):
    question=st.text_area(label='Type your question here',placeholder="What is an offer")
    button=st.form_submit_button("submit")
col1,col2=st.columns([3,2])
with col1:
    if button:

        """Search Response from indexed documents"""
        #url
        url="http://localhost:5000/ask"
        #  request body
        data = {
            'question': question
        }

        # Send a POST request with the JSON body
        response = requests.post(url, json=data)
        #parse response as a json
        response=response.json()
        message=response['message']
        results=response['results']

        #first retrieved passage and score
        passage_0=results['Passage 0:']
        score_0=results['Score 0:']
        #second retrieved passage and score
        passage_1=results['Passage 1:']
        score_1=results['Score 1:']

        #third retrived passage and score
        passage_2=results['Passage 2:']
        score_2=results['Score 2:']
        #Output the passage and their corresponding relevant scores
        st.write(f"{passage_0} Relevance_score: {score_0}\n\n  {passage_1} Relevance_score: {score_1}\n\n {passage_2} Relevance_score: {score_2}")
        
            
        print(response)
    else:
        st.warning('No question submited')
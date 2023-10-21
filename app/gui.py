import streamlit as st
import requests
from huggingface_hub import InferenceClient
#Set the page configs
st.set_page_config(page_title='Question Answering bot',page_icon='😎',layout='wide')
#image=plt.imread('app\img\gavel.jpg')


#set the title
st.title("Question Answering System for Legal Practioners ⚖⚖")
#st.image(image,caption='Youngest lawyer in Ghana',width=400,use_column_width=False)

with st.form(key='question'):
    question=st.text_area(label='Type your question here',placeholder="What is an offer")
    button=st.form_submit_button("submit")
col1,col2=st.columns([3,2])
col1.write('<h2 style="font-size: 24px;"> Search Response from indexed documents </h2>',unsafe_allow_html=True)
col2.write('<h2 style="font-size: 24px;"> large language model response </h2>',unsafe_allow_html=True)
with col1:
    if button:

       
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

with col2:
    if button:

        client = InferenceClient(token='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')
        #prompt template(alpaca template)
        prompt_template = f"""You are legal practitioner with indepth knowledge about law. write a response that correcty answers the following question

        ### question:
        {question}
        ### Response: """
        response_llm=client.text_generation(prompt=prompt_template,max_new_tokens=1000,model='tiiuae/falcon-7b-instruct')
        st.write(response_llm)
        print(response_llm)
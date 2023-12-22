from langchain.document_loaders import TextLoader, PyPDFLoader, DataFrameLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from rich.console import Console
from langchain.chains import RetrievalQA #-> for retrieval QA
from langchain.chains.question_answering import load_qa_chain #-> for load QA 
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain


import pandas as pd

import streamlit  as st
import time
import os


OPENAI_API_KEY = "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"
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY




st.title('IT-SITIO Generativo')
st.subheader('Extraemos las últimas noticias', divider='blue')

st.write(
    
'''
## 




'''
)

def load_data():
    df = pd.read_csv("../data/output.csv")
    return df




def data_extractors():
    '''
    function for run scraper
    
    '''
    data = {}
    
    df = load_data()

    
    sub_set = df[['author','title','text']][1:2]
    data['author'] = sub_set['author'].values[0]
    data['title'] = sub_set['title'].values[0]
    data['text'] = sub_set['text'].values[0]
    
    data['most_prolific'] = df['author'].value_counts()
    
    return data
        



def loader_and_splitter():
    df = load_data()
    loader = DataFrameLoader(df, page_content_column="text")
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 10000,
        chunk_overlap  = 200,
        length_function = len,
    )
    texts = text_splitter.split_documents(docs)
    return texts


def embeddor_and_retrievers(texts):
    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(texts, embeddings)
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k":5})
    
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(), 
        chain_type="map_reduce", 
        retriever=retriever, 
        return_source_documents=True)
    
    return qa







def main():    
    
    tab1, tab2 = st.tabs(["Extractors", "Intelligent Companion"])
    
    with tab1:
        st.header("Extractors")
        st.image("https://media.licdn.com/dms/image/D5612AQH9JcSLuod4_Q/article-cover_image-shrink_720_1280/0/1689851045487?e=2147483647&v=beta&t=nEzZzgvxRZJspVd6wInlH1VuEIbZi6Ls9DdNpmgbi4E", width=700)

        data = data_extractors()
        text = data['text']
        st.markdown("---")
        st.subheader('**Author**: ' + data['author'])
        st.subheader('**Title**: ' + data['title'])
        st.markdown(text)
        st.markdown("---")
        
    #st.subheader('**Most Prolific Author**: ' )
    #data['most_prolific'][:1]
    
    
    with tab2:
        st.header("Intelligent Companion")
        st.image("https://miro.medium.com/v2/resize:fit:1400/1*WKotq_wnxSmLumVfmaGAIQ.png", width=700)
       
        texts = loader_and_splitter()
        qa = embeddor_and_retrievers(texts) 
        
       
    prompt = st.chat_input("Say something")
    if prompt:
        st.write(f"User has sent the following prompt: {prompt}")
        result = qa({"query": prompt})
        result['result']



main()
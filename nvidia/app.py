import streamlit as st
import os
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings, ChatNVIDIA
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv
load_dotenv()

# Set up the NVIDIA client
os.environ["NVIDIA_API_KEY"] = os.getenv("NVIDIA_API_KEY")
client = ChatNVIDIA(
    model="nvidia/llama-3.1-nemotron-70b-instruct",
    temperature=0.5,
    top_p=1,
    max_tokens=1024,
)

def vectorize_documents():
    if "vectors" not in st.session_state:
        st.session_state.embeddings = NVIDIAEmbeddings()
        st.session_state.loader = PyPDFDirectoryLoader("./us_census")
        st.session_state.documents = st.session_state.loader.load()
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        st.session_state.split_docs = st.session_state.text_splitter.split_documents(
            st.session_state.documents[:30]
        )  
        st.session_state.vectors = FAISS.from_documents(
            st.session_state.split_docs, st.session_state.embeddings
        )

st.title("NVIDIA LLM Chatbot")

prompt=ChatPromptTemplate.from_template(
"""
Answer the questions based on the provided context only.
Please provide the most accurate response based on the question
<context>
{context}
<context>
Questions:{input}

"""
)

prompt1=st.text_input("Enter Your Question From Doduments")


if st.button("Documents Embedding"):
    vectorize_documents()
    st.write("Vector Store DB Is Ready")
import time
if prompt1:
    document_chain=create_stuff_documents_chain(llm=client,prompt=prompt)
    retriever=st.session_state.vectors.as_retriever()
    retrieval_chain=create_retrieval_chain(retriever,document_chain)
    start=time.process_time()
    response=retrieval_chain.invoke({'input':prompt1})
    print("Response time :",time.process_time()-start)
    st.write(response['answer'])

    # With a streamlit expander
    with st.expander("Document Similarity Search"):
        # Find the relevant chunks
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("--------------------------------")

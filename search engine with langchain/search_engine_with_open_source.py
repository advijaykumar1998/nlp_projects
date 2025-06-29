import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.prompts import PromptTemplate
import os
import dotenv
from dotenv import load_dotenv  
load_dotenv()

#wikipedia wrapper
api_wrapper_wiki = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=250)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper_wiki)

#arxiv wrapper
api_wrapper_arxiv = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=250)
arxiv = ArxivQueryRun(api_wrapper=api_wrapper_arxiv)

#duckduckgo wrapper
search = DuckDuckGoSearchRun(name="search")

st.title("Search Engine with Langchain and Groq")

"""
This is a search engine that uses the Groq API to search for information from Wikipedia, Arxiv, and DuckDuckGo."""

#side bar for settings
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your Grok API key", type="password")

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "You are a helpful assistant. When answering, use tools if needed, and always format the response properly.Do not make small talk. Only respond with an action or final answer."
    }]



for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt:= st.chat_input(placeholder="what is machine learning?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Initialize the Groq LLM
    llm = ChatGroq(groq_api_key=api_key, model_name= "Llama3-8b-8192", streaming=True)

    # Initialize the agent with the tools and Groq LLM
    tools = [search, wiki, arxiv]

    
    search_agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handling_tool_errors=True,
        
    )

    # Run the agent with the user input and stream the response to Streamlit
    with st.chat_message("assistant"):
        st_cn = StreamlitCallbackHandler(st.container(),expand_new_thoughts=True)

        response = search_agent.run(st.session_state.messages, callbacks=[st_cn] )
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
    
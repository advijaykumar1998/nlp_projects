import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler
from dotenv import load_dotenv

#set up the streamlit app
st.set_page_config(page_title="Text math problem solve agent and data search agent ")
st.title("Text to math problem solver with gemma 2 model")

#get the groq api key
groq_api_key = st.sidebar.text_input(label="provide the groq api key", type="password")

if not groq_api_key:
    st.info("please add your groq api key to continue")
    st.stop()

llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

##Initializing the tool
wikipedia_wrapper = WikipediaAPIWrapper()
wikipedia_tool = Tool(
    name = "Wikipedia",
    func= wikipedia_wrapper.run,
    description="tool for search tool and solving your math problem"
)

## initiliaze the math tool
math_chain = LLMMathChain.from_llm(llm=llm)
calculator = Tool(
    name="Calculator",
    func=math_chain.run,
    description="Tool answering math related question, only mathematics expression need to resolve"
    
)

prompt="""
you are the agent tasked for solving mathematical problem. logically arrive the solution and provie berief explanation and display it point wise
question: {Question}
answer:
"""

prompt_template = PromptTemplate(
    input_variables=["question"],
    template=prompt
)

## combine all the tool in the chin
chain = LLMChain(llm=llm, prompt = prompt_template)

reasioning_tool = Tool(
    name="Reasoning tool",
    func=chain.run,
    description="a tool for answering logic based and reasoning questions"
)

##initialize the agents
assistant_agent = initialize_agent(
    tools=[wikipedia_tool, calculator, reasioning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors = True
)

if "messages" not in st.session_state:
    st.session_state["messages"]=[
        {"role":"assistant","content":"Hi, i'am a Math chatbot who can answer all the maths question"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

## function to generate the response
def generate_response(question):
    response = assistant_agent.invoke({"input":question})
    return response

## let start the conversation
question=st.text_area("Enter youe question:","I have 5 bananas and 7 grapes. I eat 2 bananas and give away 3 grapes. Then I buy a dozen apples and 2 packs of blueberries. Each pack of blueberries contains 25 berries. How many total pieces of fruit do I have at the end?")

if st.button("find my answer"):
    if question:
        with st.spinner("Generate response:"):
            st.session_state.messages.append({"role":"assistant","content":question})
            st.chat_message("user").write(question)

            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            response= assistant_agent.run(st.session_state.messages, callbacks=[st_cb])

            st.session_state.messages.append({"role":"assistant","content":response})
            st.write("### response")
            st.success(response)
    else:
        st.warning("please enther the question")


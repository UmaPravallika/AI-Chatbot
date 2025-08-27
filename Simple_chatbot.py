import streamlit as st 
from config import Config
from dotenv import load_dotenv
from llm_helper import chat,stream_parser
load_dotenv()

openai_api_key=Config.OPENAI_API_KEY

st.set_page_config(
    page_title="Streamlit OPENAI Chatbot",
    initial_sidebar_state="expanded"
)
st.title("Streamlit OPENAI Chatbot")

messages=[]
if "messages" not in st.session_state : 
    st.session_state.messages=[]

# Building Sidebar :
with st.sidebar :
    st.markdown("# Chat options")

    # For selecting model : 
    model=st.selectbox("What model would you like to use",("gpt-3.5-turbo","gpt-4"))

    # For selecting uniqueness of output : 
    temparature=st.number_input("Temparature",min_value=0.1,value=0.7,max_value=1.0,step=0.1)

    # For selecting Max_token length:
    max_token_length=st.number_input("Max token length",min_value=100,value=1000,max_value=1000)



for message in st.session_state.messages :
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_prompt :=st.chat_input("What questions do you have ?"):
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role":"user","content":user_prompt})

    with st.spinner("Generating responses..."):
        llm_response=chat(user_prompt,model,temparature,max_token_length)
        stream_output=st.write_stream(stream_parser(llm_response))

        st.session_state.messages.append({"role":"assistant","content":stream_output})
    
    last_response=st.session_state.messages[len(st.session_state.messages)-1]["content"]
    if str(last_response)!=stream_output:
        with st.chat_message("assistant"):
            st.markdown(stream_output)
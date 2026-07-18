import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

# Configure the page to be centered and clean
st.set_page_config(
    page_title="Gemini AI Assistant", 
    page_icon="🤖", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

CONFIG = {'configurable': {'thread_id': 'thread_1'}}

# Initialize chat history
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# --- GEMINI STYLE LANDING PAGE ---
# If there are no messages, show the beautiful centered greeting space
if len(st.session_state['message_history']) == 0:
    # Creating vertical spacing using empty containers
    for _ in range(4):
        st.write("")
    
    # Custom HTML/CSS for that premium gradient-friendly clean text
    st.markdown(
        """
        <div style="text-align: center;">
            <h1 style="font-size: 3rem; font-weight: 500; color: #E3E6E8; margin-bottom: 10px;">
                Meet your personal AI assistant
            </h1>
            <p style="font-size: 1.2rem; color: #888888;">
                Powered by LangGraph & Gemini
            </p>
            <p style="font-size: 1.2rem; color: #888888;">
                Made by M Hamza
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

# --- CHAT HISTORY FLOW ---
# If there are messages, render them cleanly with markdown formatting
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content']) 

# --- CHAT INPUT ---
user_input = st.chat_input('Ask Gemini...')

if user_input:
    # Add user message to history and display it
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)
    
    with st.chat_message('assistant'):
        # st.write_stream automatically returns the full, concatenated string
        full_response = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(  #this returns a python generator
                {'messages': [HumanMessage(content=user_input)]},
                config = {'configurable': {'thread_id': 'thread_1'}},
                stream_mode= 'messages'
            )
        )

    # Append the full string directly to the history (with the typo fixed!)
    st.session_state['message_history'].append({'role': 'assistant', 'content': full_response})

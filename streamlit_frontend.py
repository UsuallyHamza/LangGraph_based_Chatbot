import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

CONFIG = {'configurable': {'thread_id': 'thread_1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        # st.markdown is generally preferred over st.text for chatbots to format bolding/code blocks properly
        st.markdown(message['content']) 

user_input = st.chat_input('Type here')

if user_input:
    # Add user message to history and display it
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)
    
    # 1. Get the response from the backend
    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)
    # 2. Extract the raw content
    raw_content = response['messages'][-1].content
    # 3. Check if it's a list (multimodal block) and extract just the text
    if isinstance(raw_content, list):
        ai_message = raw_content[0]['text']
    else:
        # Fallback just in case it returns a normal string
        ai_message = str(raw_content)
    
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    with st.chat_message('assistant'):
        st.markdown(ai_message)
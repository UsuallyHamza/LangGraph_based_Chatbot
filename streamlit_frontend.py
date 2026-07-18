import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid

# ----------------------Utility functions-------------------------------------- 

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread (thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)


def load_conversation (thread_id):

    return (chatbot.get_state(config={'configurable': {'thread_id': thread_id }}).values['messages'])




# Configure the page to be centered and clean
st.set_page_config(
    page_title="Gemini AI Assistant", 
    page_icon="🤖", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)



# ----------------------Session Setup-------------------------------------- 
# Initialize chat history
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_thread(st.session_state['thread_id'])



# ----------------------Sidebar UI-------------------------------------- 
st.sidebar.title('LangGraph chatbot')

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("Past Coversations")

for thread_id in st.session_state['chat_threads'][::]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = 'user'
                content_text = str(msg.content) # Ensure user message is extracted
            else:
                role = 'assistant'
                # Check if the assistant message content is the multimodal list block
                if isinstance(msg.content, list) and len(msg.content) > 0:
                    content_text = msg.content[0].get('text', '')
                else:
                    content_text = str(msg.content)
            
            # Append the clean 'content_text' variable, not the raw msg.content
            temp_messages.append({'role': role, 'content': content_text})
        
        st.session_state['message_history'] = temp_messages




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


# ----------------------Main UI-------------------------------------- 

# If there are messages, render them cleanly with markdown formatting
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content']) 

# --- CHAT INPUT ---
user_input = st.chat_input('Ask Anything...')

if user_input:
    # first Add user message to history and display it
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)
    
    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

    
    with st.chat_message('assistant'):
        # 1. Custom generator function to peel off the raw JSON data block structures
        def stream_content():
            for message_chunk, metadata in chatbot.stream( 
                {'messages': [HumanMessage(content=user_input)]},
                config= CONFIG,
                stream_mode='messages'
            ):
                content = message_chunk.content
                # Look inside the multimodal list block and yield only the pure text
                if isinstance(content, list) and len(content) > 0:
                    yield content[0].get('text', '')
                # Fallback if it returns a standard string chunk
                elif isinstance(content, str):
                    yield content

        # 2. st.write_stream consumes our generator and prints smooth text to the UI
        full_response = st.write_stream(stream_content())

    # 3. Append the clean final string response directly to history
    st.session_state['message_history'].append({'role': 'assistant', 'content': full_response})

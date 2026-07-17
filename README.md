# Agentic AI Chatbot with LangGraph & Streamlit

An interactive, memory-persistent AI chatbot built to demonstrate core Agentic AI engineering concepts. The application leverages **LangGraph** for state management, **LangChain** for LLM orchestration, and **Streamlit** for the frontend interface. It is powered by Google's highly optimized **Gemini 3.5 Flash** model.

## 🚀 Features
* **Stateful Graph Architecture:** Uses LangGraph's `StateGraph` to manage the flow of conversation iteratively.
* **Persistent Memory:** Integrates LangGraph's `MemorySaver` checkpointer to maintain thread-level conversation history, allowing the AI to remember context across continuous inputs.
* **Seamless UI Integration:** Features a clean, responsive web interface built with Streamlit's native chat elements (`st.chat_message`, `st.chat_input`).
* **Multimodal Output Handling:** Automatically parses and extracts pure text from Gemini's complex multimodal content blocks for clean UI rendering.
* **Secure Execution:** Environment variables are safely decoupled from the codebase for secure local execution and cloud deployment.

## 🛠️ Tech Stack
* **Frameworks:** LangGraph, LangChain
* **Frontend:** Streamlit
* **LLM:** Google Generative AI (`gemini-3.1-flash-lite`)
* **Environment & Package Management:** `uv`

## 📁 Project Architecture
The project is decoupled into a clear backend/frontend separation:
* `langgraph_backend.py`: Defines the state schema (`TypedDict`), configures the Google GenAI model, sets up the memory checkpointer, and compiles the `StateGraph`.
* `streamlit_frontend.py`: Manages the session state for the UI, captures user input, routes it to the compiled LangGraph backend via a `thread_id`, and safely extracts the AI's response to update the chat window.

## 💻 Local Setup & Installation

This project uses `uv` for lightning-fast dependency management.

2. Set up the virtual environment and install dependencies

Bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt


3. Configure Environment Variables
Create a .env file in the root directory and add your Google API Key:

Code snippet
GOOGLE_API_KEY=your_google_api_key_here


4. Run the Streamlit App

Bash
streamlit run 10_Chatbot_With_UI/streamlit_frontend.py


📝 License
This project is open-source and available under the MIT License.

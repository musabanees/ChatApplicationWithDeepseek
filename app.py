from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_core.language_models import LLM
from typing import Optional, List, Mapping, Any
from langchain.prompts import PromptTemplate
import requests
import json
import streamlit as st

# Custom DeepSeek LLM class
class OpenRouterDeepSeek(LLM):
    api_key: str
    model: str = "deepseek/deepseek-r1:free"
    url: str = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key=api_key, **kwargs)  

    @property
    def _llm_type(self) -> str:
        return "openrouter_deepseek"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "Maternity Chatbot"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(self.url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"API Error: {response.status_code} - {response.text}")

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"model": self.model, "api_key": "****"}  # Masked for safety

# Initialize DeepSeek LLM
api_key = "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"
llm = OpenRouterDeepSeek(api_key=api_key)

# Load Chroma vector store
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = Chroma(persist_directory="./chroma_db_multiplePage", embedding_function=embeddings)

# Define custom prompt template
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
    You are an empathetic maternity assistant designed to help pregnant women manage stress. 
    You must follow the following instructions strictly:
    1. You must provide the response from the content you receive from the chromdb. 
    2. You must not make things or provide the response which is not retrive from the chromdb.
    3. You must provide the friendly, conversational response.
    4. If there is any query that cannot be answer from knowledge base then appologise to the user and doesn't provide any responses.

    Context: {context}

    Question: {question}

    Response:
    """
)

# Setup RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt_template}
)

# Streamlit interface
st.title("Perinatal Wellbeing")
st.write("Personalised Chat Assistance")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("What’s on your mind?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


# Create a placeholder for the assistant's response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Thinking...") 
        
        # Get the response from the RAG chain
        result = qa_chain.invoke({"query": prompt})
        response = result["result"]
        
        # Replace "thinking..." with the actual response
        placeholder.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # # Get and display bot response
    # with st.chat_message("assistant"):
    #     result = qa_chain.invoke({"query": prompt})
    #     response = result["result"]
    #     st.markdown(response)
    #     st.session_state.messages.append({"role": "assistant", "content": response})
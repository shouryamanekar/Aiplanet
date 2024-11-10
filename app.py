import json
import os
import streamlit as st

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingMode
from llama_index.llms.openai import OpenAI
from copy import deepcopy
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv
import openai

# Load .env file
load_dotenv()

@st.cache_resource
def create_datastax_connection():
    
    cloud_config = {'secure_connect_bundle': 'secure-connect-aiplanet.zip'}
    with open("aiplanet_astra_test_token.json") as f:
        secrets = json.load(f)
    CLIENT_ID = secrets["clientId"]
    CLIENT_SECRET = secrets["secret"]

    auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    astra_session = cluster.connect()
    return astra_session


def main():
    st.set_page_config(page_title="Chat with your PDF using Llama 2", page_icon="🦙")
    st.header("🦙 Chat with your PDF using Llama 2 & Llama Index")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "activate_chat" not in st.session_state:
        st.session_state.activate_chat = False

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.markdown(message["content"])

    session = create_datastax_connection()

    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    # Set up the Hugging Face embedding model for indexing
    embed_model = OpenAIEmbedding(
        api_key=openai.api_key,
        mode=OpenAIEmbeddingMode.SIMILARITY_MODE,
        model="text-embedding-ada-002"
    )

    # Set up the Llama Index context with the Hugging Face model
    llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)


    Settings.llm = llm
    Settings.embed_model=embed_model
    Settings.chunk_size=256

    with st.sidebar:
        st.subheader("Upload Your PDF File")
        docs = st.file_uploader("⬆️ Upload your PDF & Click to process", accept_multiple_files=False, type=["pdf"])
        if st.button("Process"):
            with NamedTemporaryFile(dir=".", suffix=".pdf") as f:
                f.write(docs.getbuffer())
                with st.spinner("Processing"):
                    documents = SimpleDirectoryReader(".").load_data()
                    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model, llm=llm)
                    query_engine = index.as_query_engine()
                    if "query_engine" not in st.session_state:
                        st.session_state.query_engine = query_engine
                    st.session_state.activate_chat = True

    if st.session_state.activate_chat:
        if prompt := st.chat_input("Ask your question from the PDF?"):
            with st.chat_message("user", avatar="👨🏻"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "avatar": "👨🏻", "content": prompt})

            query_index_placeholder = st.session_state.query_engine
            pdf_response = query_index_placeholder.query(prompt)
            cleaned_response = pdf_response.response
            with st.chat_message("assistant", avatar="🦙"):
                st.markdown(cleaned_response)
            st.session_state.messages.append({"role": "assistant", "avatar": "🦙", "content": cleaned_response})
        else:
            st.markdown("Upload your PDFs to chat")

if __name__ == "__main__":
    main()

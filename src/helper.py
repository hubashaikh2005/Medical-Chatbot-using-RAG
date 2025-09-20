import os
from dotenv import load_dotenv
from langchain_community.embeddings import SentenceTransformerEmbeddings
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

def get_embeddings_model():
    return SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# --- Pinecone ---
def get_pinecone_index(index_name="medical-chatbot", dimension=384):
    api_key = os.getenv("PINECONE_API_KEY")
    pc = Pinecone(api_key=api_key)

    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=dimension, 
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
    return pc.Index(index_name)

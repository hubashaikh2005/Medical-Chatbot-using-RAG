from langchain_pinecone import PineconeVectorStore
from src.helper import get_embeddings_model, get_pinecone_index

def get_vectorstore(index_name="medical-chatbot"):     #Return Pinecone vectorstore
    embeddings = get_embeddings_model()
    get_pinecone_index(index_name=index_name, dimension=384)
    return PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings
    )

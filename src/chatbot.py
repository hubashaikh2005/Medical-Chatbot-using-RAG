from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
import os

def init_bot(vectorstore, template):
    retriever = vectorstore.as_retriever(
        search_type="similarity", search_kwargs={"k": 5}
    )

    hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")           
    if not hf_token:
        raise ValueError("HUGGINGFACEHUB_API_TOKEN not found in environment variables")

    llm = HuggingFaceEndpoint(
        repo_id="Qwen/Qwen3-Next-80B-A3B-Instruct", 
        task="text-generation",
        temperature=0.0,
        max_new_tokens=512,
        huggingfacehub_api_token=hf_token
        )

    chatModel = ChatHuggingFace(llm=llm)

    prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", "{input}")
    ])

    qa_chain = create_stuff_documents_chain(chatModel, prompt)
    final_chain = create_retrieval_chain(retriever, qa_chain)

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        buffer_size=3,
        return_messages=True
    )

    conv_chain = ConversationalRetrievalChain.from_llm(
        llm=chatModel,
        retriever=retriever,
        memory=memory,
        return_source_documents=False
    )

    return final_chain, memory, conv_chain

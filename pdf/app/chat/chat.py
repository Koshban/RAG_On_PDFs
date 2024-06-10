from app.chat.models import ChatArgs
from app.chat.vector_stores.pinecone import build_retriever
from langchain.chains import conversational_retrieval
from app.chat.llms.chatopenai import build_llm
from app.chat.memories.sql_memory import build_memory

def build_chat(chat_args: ChatArgs):
    retriever = build_retriever(chat_args=chat_args)
    llm = build_llm(chat_args=chat_args)
    memory = build_memory(chat_args=chat_args)
    return conversational_retrieval.from_llm(
        llm=llm,
        memory=memory,
        retriever=retriever
    )


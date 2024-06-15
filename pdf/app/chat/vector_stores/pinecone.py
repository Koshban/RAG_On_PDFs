import os
from langchain_pinecone import Pinecone
from langchain_pinecone.vectorstores import PineconeVectorStore
from app.chat.embeddings.openai import embeddings

vector_store = Pinecone(
    pinecone_api_key=os.getenv("PINECONE_API_KEY"), 
    index_name=os.getenv("PINECONE_INDEX_NAME"), 
    embedding=embeddings, 
    namespace=os.getenv("PINECONE_ENV_NAME")
    )

def build_retriever(chat_args, k):
    search_kwargs = {
        "filter" : {"pdf_id" : chat_args.pdf_id },
        "k" : k
        }
    return vector_store.as_retriever(
        search_kwargs=search_kwargs
    )



from app.chat.models import ChatArgs
from app.chat.vector_stores.pinecone import build_retriever
from app.chat.llms.chatopenai import build_llm
from app.chat.memories.sql_memory import build_memory
from app.chat.chains.retrieval import StreamingConversationalRetrievalChain
from langchain_openai import ChatOpenAI

def build_chat(chat_args: ChatArgs):
    retriever = build_retriever(chat_args=chat_args)
    llm = build_llm(chat_args=chat_args)
    condense_question_llm = ChatOpenAI(streaming=False) # This version is created to use a sepaarte CHatOpenAI for the condense quesion chain, so as to be bale to leverage the 
    # StreamingHandler only for the Combine Docs Chain and NOT the Condense Question Chain ( which does the summarization during Streaming)
    memory = build_memory(chat_args=chat_args)

    return StreamingConversationalRetrievalChain.from_llm(
        llm=llm,
        condense_question_llm=condense_question_llm, # To detach Streaming Handler from Condense Question Chain
        memory=memory,
        retriever=retriever
    )


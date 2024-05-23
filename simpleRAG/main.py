""" Based on using Vector DB and RAG to extract relevant data from the Facts.txt file and asnwer quesries based on that data"""
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
#from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
#from langchain.chains import LLMChain, SequentialChain
import argparse
import os

def setup_env(file: str):
    load_dotenv(find_dotenv())
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    embeddings = OpenAIEmbeddings()
    emb = embeddings.embed_query("My name is Kaushik") # How to query embeddings manually
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=200, chunk_overlap=0)
    loader = TextLoader(f'{BASE_DIR}\\{file}')
    llm = ChatOpenAI()
    docs = loader.load_and_split(text_splitter=text_splitter)
    # Embedding DB/Vector Store Chroma
    db = Chroma.from_documents(
        docs, embedding=embeddings, persist_directory="emb"
    )
    return db

def doing_search(db):
    print(f"DB is {db}")
    user_query = input("What is your Query ? : ")
    print(f"Query is : {user_query}")
    #results = db.similarity_search_with_score("{user_query}", k=2)
    results = db.similarity_search(f"{user_query}", k=4) # No score, only contents
    for result in results:
        print("\n", result.page_content) # Actual content


def get_args() -> str:
    parser = argparse.ArgumentParser(description="File from whcih Data is to be Read")
    parser.add_argument('-f', '--file', default="Facts.txt", required=False, type=str, help="File from whcih Data is to be Read")
    myargs = parser.parse_args()
    return myargs.file

if __name__ == "__main__":
    filename = get_args()
    print(f"Filename is : {filename}")
    db = setup_env(file=filename)
    doing_search(db=db)


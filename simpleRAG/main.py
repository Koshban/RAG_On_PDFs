""" Based on using Vector DB and RAG to extract relevant data from the Facts.txt file and asnwer quesries based on that data"""
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.document_loaders import TextLoader
from langchain.chains import LLMChain, SequentialChain
import argparse
import os

def setup_env(file: str):
    load_dotenv(find_dotenv())
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    loader = TextLoader(f'{BASE_DIR}\\Facts.txt')
    llm = ChatOpenAI()
    docs = loader.load()
    #print(docs)


def get_args() -> str:
    parser = argparse.ArgumentParser(description="File from whcih Data is to be Read")
    parser.add_argument('-f', '--file', default="Facts.txt", required=False, type=str, help="File from whcih Data is to be Read")
    myargs = parser.parse_args()
    return myargs.file




if __name__ == "__main__":
    filename = get_args()
    print(f"Filename is : {filename}")
    setup_env(file=filename)


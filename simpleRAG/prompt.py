""" Based on using Vector DB and RAG to extract relevant data from the Facts.txt file and asnwer quesries based on that data"""
from dotenv import load_dotenv, find_dotenv
import langchain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA    
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.question_answering import load_qa_chain
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.vectorstores import VectorStoreRetriever
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from redundant_filter_retriever import RedundantFilterRetriever
import argparse
import os
import logging
#langchain.debug = True

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_env(file: str):
    load_dotenv(find_dotenv())  
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
    embeddings = OpenAIEmbeddings()       
    persist_directory="emb" 
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=200, chunk_overlap=0)
    loader = TextLoader(f'{BASE_DIR}\\{file}')
    docs = loader.load_and_split(text_splitter=text_splitter)
    # Embedding DB/Vector Store Chroma. Just creating an instance, We are NOT Loading any docs here 
    # Check if the vector store already exists
#    if os.path.exists(os.path.join(persist_directory, "index")):
    if os.path.exists(f'{BASE_DIR}\\{persist_directory}'):
        # Load the existing vector store
        logger.info("Loading existing vector store")
        db = Chroma(
            embedding_function=embeddings, persist_directory=persist_directory
        )
    else:
        # Load the facts from the text file into a new vector Store
        logger.info("Creating new vector store and adding facts")
        db = Chroma.from_documents(
        docs, embedding=embeddings, persist_directory=persist_directory
        )

    chat = ChatOpenAI(verbose=True, model=os.getenv("OPENAI_MODEL", "gpt-4"))
    # Set up the retriever
    #retriever = VectorStoreRetriever(vectorstore=db, top_k=5)
    retreiver = RedundantFilterRetriever(embeddings=embeddings, chroma=db)
    #retriever = db.as_retriever()
    qa_chain= load_qa_chain(llm=chat, 
                            #chain_type="stuff"
                            #chain_type="map_reduce"
                            chain_type="map_rerank")
    chain = RetrievalQA(
        retriever=retriever,
        combine_documents_chain=qa_chain )
    logger.info(f"Chain is : {chain}")
    logger.info(f"OpenAI Model being used is : {chat.model_name}")
    return chain

def doing_search(chain):
    try:
        user_query = input("What is your Query ? : ")
        logger.info(f"Received query: {user_query}")
        result = chain.invoke(user_query)
    except KeyboardInterrupt:
        print("\n **** Exiting Now, Bbye!! *******")
        exit()
    return result

def log_chain_messages(chain):
    try:
        # Access the StuffDocumentsChain
        stuff_chain = chain.combine_documents_chain
        
        # Access the LLMChain from the StuffDocumentsChain
        llm_chain = stuff_chain.llm_chain
        
        # Access the ChatPromptTemplate from the LLMChain
        prompt_template = llm_chain.prompt
        
        # Extract the messages
        messages = prompt_template.messages
        
        # Log the messages
        for message in messages:
            if isinstance(message, SystemMessagePromptTemplate):
                logger.info(f"System Message: {message.prompt.template}")
            elif isinstance(message, HumanMessagePromptTemplate):
                logger.info(f"Human Message: {message.prompt.template}")
            else:
                logger.info(f"Unknown Message Type: {message}")
    except AttributeError as e:
        logger.error(f"Error accessing chain messages: {e}")

def get_args() -> str:
    parser = argparse.ArgumentParser(description="File from whcih Data is to be Read")
    parser.add_argument('-f', '--file', default="Facts.txt", required=False, type=str, help="File from whcih Data is to be Read")
    myargs = parser.parse_args()
    return myargs.file

if __name__ == "__main__":
    filename = get_args()
    print(f"Filename is : {filename}")
    chain = setup_env(file=filename)
    result = doing_search(chain=chain)
    # Log the input and output
    log_chain_messages(chain)
    logger.info(f"Query Was   : {result["query"]}")
    logger.info(f"Response Is : {result["result"]}")




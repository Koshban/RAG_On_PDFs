"""
    Generate and store embeddings for the given pdf

    1. Extract text from the specified PDF.
    2. Divide the extracted text into manageable chunks.
    3. Generate an embedding for each chunk.
    4. Persist the generated embeddings.

    :param pdf_id: The unique identifier for the PDF.
    :param pdf_path: The file path to the PDF.

    Example Usage:

    create_embeddings_for_pdf('123456', '/path/to/pdf')
"""
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from logger import get_logger

# Get the logger for the current module
logger = get_logger(__name__)

def create_embeddings_for_pdf(pdf_id: str, pdf_path: str):
    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=500,
    #     chunk_overlap=100
    # )

    # loader=PyPDFLoader(pdf_path)

    # docs = loader.load_and_split(text_splitter=text_splitter)
    # logger.debug(f'Docs are {docs}')
    pass




    

from typing import List
from langchain.document_loaders import ConfluenceLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os

def load_all_confluence_pages(loader: ConfluenceLoader, space_key: str, max_pages_per_request: int = 100) -> List[Document]:
    """Loads all Confluence pages from a space recursively.

    Args:
        loader (ConfluenceLoader): An initialized ConfluenceLoader instance.
        space_key (str): The key of the Confluence space.
        max_pages_per_request (int, optional): The maximum number of pages to 
                                               request at a time. Defaults to 100.

    Returns:
        List[Document]: A list of all loaded Confluence pages as Document objects.
    """
    all_docs = []
    start_page = 0
    while True:
        docs = loader.load(
            space_key=space_key, 
            max_pages=max_pages_per_request, 
            start_page=start_page, 
            include_attachments=False
        )
        if not docs:  # If no more pages are returned, break the loop
            break
        all_docs.extend(docs)
        start_page += max_pages_per_request

    return all_docs

def _load(metadata):
    loader = ConfluenceLoader(
        url='myurl', 
        token=os.getenv('CONF_TOKEN'), 
        cloud=False, 
        space_key=os.getenv('KEY')
    )

    docs = load_all_confluence_pages(loader, space_key=os.getenv('KEY'))

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200, add_start_index=True)
    splitters = text_splitter.split_documents(docs)
    return splitters

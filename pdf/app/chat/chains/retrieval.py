from langchain.chains import conversational_retrieval
from pdf.app.chat.chains.streamable import StreamableChain
from app.chat.chains.traceable import TraceableChain

''' Extend the StreamableChain with conversationalRetrieval class so as to be able to create a Streaming Conversational Class Overwrite'''

class StreamingConversationalRetrievalChain(TraceableChain, StreamableChain, conversational_retrieval):
    pass


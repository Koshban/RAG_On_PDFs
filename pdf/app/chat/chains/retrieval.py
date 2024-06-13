from langchain.chains import conversational_retrieval
from pdf.app.chat.chains.streamable import StreamableChain

''' Extend the StreamableChain with conversationalRetrieval class so as to be able to create a Streaming Conversational Class Overwrite'''

class StreamingConversationalRetrievalChain(StreamableChain, conversational_retrieval):
    pass


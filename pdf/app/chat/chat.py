from app.chat.models import ChatArgs

from app.chat.chains.retrieval import StreamingConversationalRetrievalChain
from langchain_openai import ChatOpenAI
# from app.chat.vector_stores.pinecone import build_retriever
# from app.chat.llms.chatopenai import build_llm
# from app.chat.memories.sql_memory import build_memory
from app.chat.vector_stores import retriever_map
from app.chat.memories import memory_map
from app.chat.llms import llm_map
from app.web.api import set_conversation_components, get_conversation_components
import random
from app.chat.score import random_component_by_score



def select_component(component_type, component_map, chat_args):
    ''' Below  code is to use a random retriever from our set/map of retrievers, and thus we need to store the conversation id to ensure one conversation uses one retriever only
    if you dont need to use such functionality, just use the below line a retriever
    retriever = build_retriever(chat_args=chat_args)
    '''
    components = get_conversation_components(chat_args.conversation_id)
    previous_component = components[component_type]
    if previous_component:
        # NOT the first message of the conversation, so we need to continue using the same msg
        builder = component_map[previous_component]
        return previous_component, builder(chat_args=chat_args)
    else:
        # First message of the conversation, pick any retriever to use
        # random_name = random.choice(list(component_map.keys()))
        random_name = random_component_by_score(component_type, component_map)
        builder = component_map[random_name]
        return random_name, builder(chat_args=chat_args)

def build_chat(chat_args: ChatArgs):
#    llm = build_llm(chat_args=chat_args)
#    memory = build_memory(chat_args=chat_args)
#    retriever = build_retriever(chat_args=chat_args)
    retriever_name, retriever = select_component(
        component_type="retriever", component_map=retriever_map, chat_args=chat_args
    )
    llm_name, llm = select_component(
        component_type="llm", component_map=llm_map, chat_args=chat_args
    )
    memory_name, memory = select_component(
        component_type="memory", memory_map=memory_map, chat_args=chat_args
    )

    set_conversation_components(
            conversation_id=chat_args.conversation_id,
            llm=llm_name,
            memory=memory_name,
            retriever=retriever_name
            )
    
    condense_question_llm = ChatOpenAI(streaming=False) # This version is created to use a sepaarte CHatOpenAI for the condense quesion chain, so as to be bale to leverage the 
    # StreamingHandler only for the Combine Docs Chain and NOT the Condense Question Chain ( which does the summarization during Streaming)
    
    return StreamingConversationalRetrievalChain.from_llm(
        llm=llm,
        condense_question_llm=condense_question_llm, # To detach Streaming Handler from Condense Question Chain
        memory=memory,
        retriever=retriever,
        metadata=chat_args.metadata        
    )


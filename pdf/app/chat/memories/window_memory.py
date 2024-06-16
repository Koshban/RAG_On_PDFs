from langchain.memory import ConversationBufferWindowMemory
from app.chat.memories.history.sql_history import SqlMessageHistory

def window_buffer_build_memory(chat_args):
    return ConversationBufferWindowMemory(
        chat_memory=SqlMessageHistory(
            conversation_id=chat_args.conversation_id
        ),
        return_messages=True,
        memory_key="chat_history",
        output_key="answer", # In out put Variables Dict, Answer is the key against which output will be stored
        k=5
    )
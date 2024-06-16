from app.chat.memories.history.sql_history import SqlMessageHistory
from langchain.memory import ConversationBufferMemory

def build_memory(chat_args):
    return ConversationBufferMemory(
        chat_memory=SqlMessageHistory(
            conversation_id=chat_args.conversation_id
        ),
        return_messages=True,
        memory_key="chat_history",
        output_key="answer" # In out put Variables Dict, Answer is the key against which output will be stored
    )
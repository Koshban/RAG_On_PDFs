
""" Based on Simple Conversational template"""
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory, FileChatMessageHistory, ConversationSummaryMemory, ConversationSummaryBufferMemory
from dotenv import load_dotenv
import os

# Setting Up environment
load_dotenv()
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)

def  yak_away_as_much_as_you_like():
    chat = ChatOpenAI(verbose=True) # To Create the Initial OpenAI Object and added verbose=True to if you want to debug what's going on inside the wrapper
    # SetUp The Langchain "memory" first, the placeholder for the conversation history and context. Bit it has size limits and obviously costs more and more.
    # chatmemory = ConversationBufferMemory(memory_key="convhistory", return_messages=True, chat_memory=FileChatMessageHistory(f"{BASE_DIR}\\chattinghistory.json"))
    # Or you can use a SummaryMemory which summarizes and stores the conversations up-to-that-point for every iteration. That is stored at every point as a SystemMessage
    chatmemory = ConversationSummaryBufferMemory(memory_key="convhistory", return_messages=True, llm=chat, max_token_limit=40)
    
    prompt = ChatPromptTemplate(
        input_variables=["content", "convhistory"],
        messages=[
            MessagesPlaceholder(variable_name="convhistory" ),
            HumanMessagePromptTemplate.from_template("{content}")
        ]
    )

    chain = LLMChain(
        llm=chat,
        prompt=prompt,
        memory=chatmemory,
        verbose=True # To check whats going on inside the wrapper
    )

    while True:
        try:
            content = input(">> ")
            result = chain({"content": content})
            messages =  chatmemory.chat_memory.messages
            summary = chatmemory.moving_summary_buffer
            print(f"Result is : {result["text"]}")
            # print(f"Messages is : {messages}")
            # print(f"Summary is : {summary}")
            # print(f"Chatmemory is now : {chatmemory}")

        except KeyboardInterrupt:
            print("\n **** Exiting Now, Bbye!! *******")
            exit()

if __name__ == "__main__":
    yak_away_as_much_as_you_like()
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
# from langchain.chains import LLMChain
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

chat = ChatOpenAI(streaming=True, verbose=True)

prompt =  ChatPromptTemplate.from_messages([
    ("human", "{content}")
])

# chain = LLMChain(llm=chat, prompt=prompt)
chain = prompt | chat
output = chain.stream(input="Tell me a Joke about Animals")
print(output)

# messages = prompt.format_messages(content="Tell me a Joke about Animals")

# output = chat.stream(messages)
# print(output)
for message in chain.stream(input={"content" : "Tell me a Joke about Animals"}): # chat.stream overrides ChatOpenAI(streaming=False) so it will stream irrespective of the above Flag is True or False
    print(message)
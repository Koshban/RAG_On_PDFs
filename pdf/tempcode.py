from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv, find_dotenv
from typing import Any
from uuid import UUID
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.outputs import ChatGenerationChunk, GenerationChunk, LLMResult
from queue import Queue
from threading import Thread
 
load_dotenv(find_dotenv())


class StreamingHandler(BaseCallbackHandler):
    def __init__(self, queue) -> None:
        self.queue = queue
        
    # def on_llm_new_token(self, token: str, *, chunk: GenerationChunk | ChatGenerationChunk | None = None, run_id: UUID, parent_run_id: UUID | None = None, **kwargs: Any) -> Any:
    #     return super().on_llm_new_token(token, chunk=chunk, run_id=run_id, parent_run_id=parent_run_id, **kwargs)
    def on_llm_new_token(self, token, **kwargs):
        self.queue.put(token)
    
    # def on_llm_end(self, response: LLMResult, *, run_id: UUID, parent_run_id: UUID | None = None, **kwargs: LLMChain) -> LLMChain:
    #     return super().on_llm_end(response, run_id=run_id, parent_run_id=parent_run_id, **kwargs)
    
    def on_llm_end(self, response, **kwargs):
        self.queue.put(None)
    
    def on_llm_error(self, error: BaseException, *, run_id: UUID, parent_run_id: UUID | None = None, **kwargs: LLMChain) -> LLMChain:
        self.queue.put(None)
        return super().on_llm_error(error, run_id=run_id, parent_run_id=parent_run_id, **kwargs)



chat = ChatOpenAI(
    streaming=True, 
    verbose=True
#    ,callbacks=[StreamingHandler()]
    )

prompt =  ChatPromptTemplate.from_messages([
    ("human", "{content}")
])

''' Base Streaming Class that would work for every type of Chains. We can just call it
with overwrite in different classes e.g. below '''
class StreamableChain:
    def stream(self, input: dict):
        queue = Queue() # An individual Queue for every session/object
        handler = StreamingHandler(queue=queue)

        def task():
            self(input, callbacks=[handler])
    
        Thread(target=task).start()  # Use a Thread utilizing concurrency so as to force the LLMChain to execute as it gets the chunks and not wait till the entire message is returned

        while True:
            try:
                token = queue.get()
                if token is None:
                    break
                yield token
            except KeyboardInterrupt:
                print("KeyBoard Interrupt Received")
                exit()

''' To overwrite CUtom Class above , extending it top LLMChain as that is what we are using here'''
class StreamingChain(StreamableChain, LLMChain):
    pass

chain = StreamingChain(llm=chat, prompt=prompt)
input = {"content" : "Tell me a Joke about Animals"}

# chain = LLMChain(llm=chat, prompt=prompt)
# chain = prompt | chat
# output = chain.invoke(input="Tell me a Joke about Animals")
#print(output)

# messages = prompt.format_messages(content="Tell me a Joke about Animals")

# output = chat.stream(messages)
# print(output)
for message in chain.stream(input = {"content" : "Tell me a Joke about Animals"}): # chat.stream overrides ChatOpenAI(streaming=False) so it will stream irrespective of the above Flag is True or False
    print(message)
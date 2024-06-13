
from typing import Dict, List, Any
from dotenv import load_dotenv, find_dotenv
from uuid import UUID
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import LLMChain
from langchain_core.messages import BaseMessage


 
load_dotenv(find_dotenv())


class StreamingHandler(BaseCallbackHandler):
    def __init__(self, queue) -> None:
        self.queue = queue
        self.streaming_run_ids = set()
    
    def on_chat_model_start(self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], *, run_id: UUID, parent_run_id: UUID | None = None, tags: List[str] | None = None,
                             metadata: Dict[str, Any] | None = None, **kwargs: LLMChain) -> LLMChain:
        if serialized["kwargs"]["streaming"]: # Store run_id of only the Streaming ChatOpenAI Model
            self.streaming_run_ids.add(run_id)
        # return super().on_chat_model_start(serialized, messages, run_id=run_id, parent_run_id=parent_run_id, tags=tags, metadata=metadata, **kwargs)
        
    # def on_llm_new_token(self, token: str, *, chunk: GenerationChunk | ChatGenerationChunk | None = None, run_id: UUID, parent_run_id: UUID | None = None, **kwargs: Any) -> Any:
    #     return super().on_llm_new_token(token, chunk=chunk, run_id=run_id, parent_run_id=parent_run_id, **kwargs)
    def on_llm_new_token(self, token, **kwargs):
        self.queue.put(token)
    
    # def on_llm_end(self, response: LLMResult, *, run_id: UUID, parent_run_id: UUID | None = None, **kwargs: LLMChain) -> LLMChain:
    #     return super().on_llm_end(response, run_id=run_id, parent_run_id=parent_run_id, **kwargs)
    
    def on_llm_end(self, response, run_id, **kwargs):
        if run_id in self.streaming_run_ids.add(run_id): # Add None to indicate not to read Queue anymore, only for the Streaming Model
            self.queue.put(None)
            self.streaming_run_ids.remove(run_id)
    
    def on_llm_error(self, error: BaseException, *, run_id: UUID, parent_run_id: UUID | None = None, **kwargs: LLMChain) -> LLMChain:
        self.queue.put(None)
        return super().on_llm_error(error, run_id=run_id, parent_run_id=parent_run_id, **kwargs)




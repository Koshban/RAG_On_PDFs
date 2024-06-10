from typing import Any
from uuid import UUID
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.outputs import ChatGenerationChunk, GenerationChunk
 


class StreamingHandler(BaseCallbackHandler):
    # def on_llm_new_token(self, token: str, *, chunk: GenerationChunk | ChatGenerationChunk | None = None, run_id: UUID, parent_run_id: UUID | None = None, **kwargs: Any) -> Any:
    #     return super().on_llm_new_token(token, chunk=chunk, run_id=run_id, parent_run_id=parent_run_id, **kwargs)
    def on_llm_new_token(self, token, **kwargs):
        print(token)
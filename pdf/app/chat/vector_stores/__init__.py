from .pinecone import build_retriever 
from functools import partial

retriever_map = {
    "pinecode_1" : partial(build_retriever, k=1),
    "pinecode_2" : partial(build_retriever, k=2),
    "pinecode_3" : partial(build_retriever, k=3),
}

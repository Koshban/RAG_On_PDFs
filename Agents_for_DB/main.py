""" U can Use transform.tools/json-to-json-schema or Google generate a JSON Schema to help with the JSON Object schema formation"""
from dotenv import load_dotenv, find_dotenv
import langchain
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor, initialize_agent, AgentType, create_openai_functions_agent
from langchain.schema import SystemMessage
from tools.sql import run_query_tool, list_tables, describe_tables_tool
import argparse
import os
import logging
langchain.debug = True

def get_args():
    parser = argparse.ArgumentParser(description="Provide the query you want answered by the ChatBot")
    parser.add_argument('-q', '--query', default='How many users are in the database?', type=str, required=False, help="The query that needs answered by ChatBot")
    myargs = parser.parse_args()
    return myargs.query

def setup_env():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    #Load environment
    load_dotenv(find_dotenv())
    BASE_DIR=os.path.dirname(os.path.abspath(__file__))
    

def get_agent_running():
    chat = ChatOpenAI(verbose=True, model=os.getenv("OPENAI_MODEL", "gpt-4"))
    tables = list_tables()
    #print(f"Tables are : {tables}")
    prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content=(
        "You are an AI agent that has access to a SQLite Database.\n"
        f"The Database has tables of : {tables}\n"
        "Do not make any assumptions about what tables or what columns exist "
        "Instead, use the 'describe_tables_tool' function."
            )
        ),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
        ]
    )

    tools = [run_query_tool, describe_tables_tool]

    # agent = OpenAIFunctionsAgent(
    #     llm=chat,
    #     prompt=prompt,
    #     tools=tools
    # )
    # agent_executor = AgentExecutor( # Runs a Loop with the AGent till the result is not a Function Call
    #     agent=agent,
    #     verbose=True,
    #     tools=tools
    # )

    agent_executor = initialize_agent( # replacing the above manual initialization and executor with a single function
        llm=chat,
        verbose=True,
        tools=tools,
        agent=AgentType.OPENAI_FUNCTIONS,
        prompt=prompt
    )

    return agent_executor

def execute_agent(execagent, query: str):
    logging.info(f"Query is: {query}")
    execagent(f'{query}')

if __name__ == "__main__":
    query=get_args()
    setup_env()
    executor=get_agent_running()
    execute_agent(execagent=executor, query=query)

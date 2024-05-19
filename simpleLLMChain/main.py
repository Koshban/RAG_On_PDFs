""" Based on Simple Completion template"""
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
import argparse

load_dotenv() # Load environment variables from .env file.


def callOpenAI(language: str, task: str) -> tuple:
    #llm = OpenAI()

    code_prompt = PromptTemplate(
        template = "Write a very short {language} function that will {task}",
        input_variables = ["language", "task"]
    )

    testing_prompt = PromptTemplate(
        template = "Write Two UnitTests in {language} that will Test the code :\n{code}",
        input_variables = ["language", "code"]
    )

    code_chain = LLMChain(
        llm = llm,
        prompt = code_prompt,
        output_key = "code"
    )

    test_chain = LLMChain(
        llm = llm,
        prompt = testing_prompt,
        output_key = "test"
    )

    chain = SequentialChain(
        chains=[code_chain, test_chain], # In the same sequence as the flow
        input_variables=["language", "task"], # My main Inputs
        output_variables=["language", "code", "test"] # Final Outputs I am interested to see, coming out of the second/final chain
    )

    result = chain({
        "language" : language,
        "task" : task
    })
    print(result)
    return (result["language"], result["code"], result["test"])

def get_args() -> tuple:
    parser = argparse.ArgumentParser(description="Command Line Arguments to LLMChain")
    parser.add_argument('-l', '--language', required=False, type=str, default="Python", help='The Language in which to program the "task"')
    parser.add_argument('-t', '--task', type=str, required=False, default="Print the first 10 Prime Numbers", help="The Task that needs to be avhieved by LangChain")
    myargs = parser.parse_args()
    return (myargs.language, myargs.task)

if __name__ == "__main__":
    language, task = get_args()    
    #print(f'Language is ** {language}**  and Task to be Achieved is ** {task} **')
    language, task = get_args()
    llm = OpenAI()
    language, code, test = callOpenAI(language=language, task=task )
    print("-" * 40, f"Language Used is : {language}", "-" * 80, "\n\n")
    print("-" * 40, "Code", "-" * 40)
    print(f"{code}")
    #check_callOpenAI(language=language, code=code)
    print("-" * 40, "Tests", "-" * 40)
    print(f"{test}")
    print("-" * 40, "Completed", "-" * 40)
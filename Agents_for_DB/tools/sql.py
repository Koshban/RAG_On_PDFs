import sqlite3
from langchain.tools import Tool
from pydantic.v1 import BaseModel
from typing import List

connection = sqlite3.connect("db.sqlite")

def list_tables():
    cursor = connection.cursor()
    cursor.execute("Select name from sqlite_master where type='table';")
    rows=cursor.fetchall()
    #print(f"Rows inside the list_tables func is ' {rows}")
    return "\n".join(row[0] for row in rows if row[0] is not None)


def run_sqlite_query(query: str):
    cursor = connection.cursor()
    try:
        cursor.execute(query)    
        return cursor.fetchall()
    except sqlite3.OperationalError as err:
        return f'Error occurred: {str(err)}'
    
def describe_tables(table_names: str):
    cursor = connection.cursor()
    tables = ', '.join("'" + table + "'" for table in table_names)
    rows = cursor.execute(f"select sql from sqlite_master where type='table' and name in ({tables});")
    return "\n".join(row[0] for row in rows if row[0] is not None)

class RunQueryArgsSchema(BaseModel):
    query: str

run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run a sqlite query",
    func=run_sqlite_query,
    args_schema=RunQueryArgsSchema)

class DescribeTablesArgsSchema(BaseModel):
    table_names: List[str]

describe_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of tale names, returns the schema of those tables ",
    func=describe_tables)


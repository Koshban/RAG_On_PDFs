from langchain.tools import StructuredTool
from pydantic.v1 import BaseModel
import os
BASE_DIR=os.path.dirname(os.path.abspath(__file__))


def write_report(filename: str, html: str):
    with open(file=f'{BASE_DIR}\\..\\{filename}', mode='w') as f_write:
        f_write.write(html)


class WriteReportArgsSchema(BaseModel):
    filename: str
    html: str


write_report_tool = StructuredTool.from_function(
    name="write_report",
    description="Write an HTML file to disk. Use this tool whenever someone asks for a report.",
    func=write_report,
    args_schema=WriteReportArgsSchema
)

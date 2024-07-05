from typing import List

from langchain_core.tools import BaseToolkit
from langchain_core.pydantic_v1 import Field
from langchain_community.tools import BaseTool

from tools import Interpreter

class InterpreterToolkit(BaseToolkit):
    """Toolkit for the interpreter."""

    api_url: str = Field(default="http://localhost:8001")

    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        toolkit = Interpreter(api_url=self.api_url).toolkit()
        return toolkit
  
if __name__ == "__main__":
	toolkit = InterpreterToolkit(api_url="http://localhost:8001")
	tools = toolkit.get_tools()
	result = tools[0].run({"session_id": "test", "code": "print('Hello, World!')"})
	print(">>> Tools: ", tools)
	print(">>> Result: ", result)
import httpx
import logging
from typing import List
from langchain.tools import StructuredTool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import ToolException

########################################################
## Model
########################################################
class ExecuteSchema(BaseModel):
    session_id: str = Field(..., description="The session ID")
    code: str = Field(..., description="The code to execute")
    env: dict = Field(default={}, description="The environment variables")
    
class InstallSchema(BaseModel):
    session_id: str = Field(..., description="The session ID")
    packages: List[str] = Field(..., description="The packages to install")
    
class TerminateSchema(BaseModel):
    session_id: str = Field(..., description="The session ID")
    
########################################################
## Class
########################################################
class Interpreter:
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        
    def install(self, session_id: str, packages: List[str]):
        url = f"{self.api_url}/install"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "session_id": session_id,
            "packages": packages
        }

        response = httpx.post(url, headers=headers, json=data)
        if response.status_code == 200:
            logging.info("Packages installed successfully:", response.json())
            return response.json()
        else:
            logging.error("Error installing packages:", response.status_code, response.text)
            raise ToolException(f"Error: {response.status_code} {response.text}")
        
    def execute(self, session_id: str, code: str ):
        url = f"{self.api_url}/execute"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "session_id": session_id,
            "code": code
        }
        
        response = httpx.post(url, headers=headers, json=data)
        if response.status_code == 200:
            logging.info("Success:", response.json())
            return response.json()
        else:
            logging.error("Error:", response.status_code, response.text)
            raise ToolException(f"Error: {response.status_code} {response.text}")
        
    def terminate(self, session_id: str):
        url = f"{self.api_url}/terminate"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "session_id": session_id
        }

        response = httpx.post(url, headers=headers, json=data)
        if response.status_code == 200:
            logging.info("Session terminated successfully:", response.json())
            return response.json()
        else:
            logging.error("Error terminating session:", response.status_code, response.text)
            raise ToolException(f"Error: {response.status_code} {response.text}")
    

        
    def toolkit(self):
        execute_tool = StructuredTool.from_function(
            args_schema=ExecuteSchema,
            func=self.execute,
            name="execute_code",
            description="Use this tool to execute python code.",
        )
        install_tool = StructuredTool.from_function(
            args_schema=InstallSchema,
            func=self.install,
            name="install",
            description="Use this tool to install python packages.",
        )
        terminate_tool = StructuredTool.from_function(
            args_schema=TerminateSchema,
            func=self.terminate,
            name="terminate",
            description="Use this tool to terminate the session.",
        )
        return [
            execute_tool,
            install_tool,
            terminate_tool,
        ]
########################################################
## Tool
########################################################
if __name__ == "__main__":
    result = Interpreter(api_url="http://localhost:8001").execute().run({
        "session_id": "test",
        "code": "print('Hello, World!')"
    })
    print(result)
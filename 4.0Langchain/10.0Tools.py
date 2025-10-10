# There are both inbuit tools and Custom tool 
# Example Inbuilt tools  -> 

# !pip install langchain langchain-core langchain-community pydantic duckduckgo-search langchain_experimental
# Built-in Tool - DuckDuckGo Search
from langchain_community.tools import DuckDuckGoSearchRun

search_tool = DuckDuckGoSearchRun()
results = search_tool.invoke('top news in india today')

print(results) #The Chinese Foreign Ministry spokesperson Guo Jiakun has condemned the terrorist attack in Jammu and Kashmir's ...
print(search_tool.name)
print(search_tool.description)
print(search_tool.args)
# duckduckgo_search
# A wrapper around DuckDuckGo Search. Useful for when you need to answer questions about current events. Input should be a search query.
# {'query': {'description': 'search query to look up', 'title': 'Query', 'type': 'string'}}

# Built-in Tool - Shell Tool
from langchain_community.tools import ShellTool

shell_tool = ShellTool()
results = shell_tool.invoke('ls')

print(results)


# Custom tools
from langchain_core.tools import tool
# Step 1,2 - create function,add type hints
def multiply(a: int, b:int) -> int:
    """Multiply two numbers"""
    return a*b

# Step 3 - add tool decorator
@tool
def multiply(a: int, b:int) -> int:
    """Multiply two numbers"""
    return a*b

result = multiply.invoke({"a":3, "b":5})
print(result) # 15

print(multiply.name)
print(multiply.description)
print(multiply.args)
print(multiply.args_schema.model_json_schema())
# multiply
# Multiply two numbers
# {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}
# {'description': 'Multiply two numbers', 'properties': {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}, 'required': ['a', 'b'], 'title': 'multiply', 'type': 'object'}

# Another custom tool (Structured tool)
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
class MultiplyInput(BaseModel):
    a: int = Field(required=True, description="The first number to add")
    b: int = Field(required=True, description="The second number to add")
def multiply_func(a: int, b: int) -> int:
    return a * b
multiply_tool = StructuredTool.from_function(
    func=multiply_func,
    name="multiply",
    description="Multiply two numbers",
    args_schema=MultiplyInput
)
result = multiply_tool.invoke({'a':3, 'b':3})

print(result)
print(multiply_tool.name)
print(multiply_tool.description)
print(multiply_tool.args)
# 9
# multiply
# Multiply two numbers
# {'a': {'description': 'The first number to add', 'required': True, 'title': 'A', 'type': 'integer'}, 'b': {'description': 'The second number to add', 'required': True, 'title': 'B', 'type': 'integer'}}


# Method 3 - Using BaseTool Class
from langchain.tools import BaseTool
from typing import Type
# arg schema using pydantic

class MultiplyInput(BaseModel):
    a: int = Field(required=True, description="The first number to add")
    b: int = Field(required=True, description="The second number to add")
class MultiplyTool(BaseTool):
    name: str = "multiply"
    description: str = "Multiply two numbers"

    args_schema: Type[BaseModel] = MultiplyInput

    def _run(self, a: int, b: int) -> int:
        return a * b

multiply_tool = MultiplyTool()
result = multiply_tool.invoke({'a':3, 'b':3})

print(result)
print(multiply_tool.name)
print(multiply_tool.description)
print(multiply_tool.args)
# 9
# multiply
# Multiply two numbers
# {'a': {'description': 'The first number to add', 'required': True, 'title': 'A', 'type': 'integer'}, 'b': {'description': 'The second number to add', 'required': True, 'title': 'B', 'type': 'integer'}}


# Toolkit
# Club multiple tols 
# Custom tools
@tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

class MathToolkit:
    def get_tools(self):
        return [add, multiply]

toolkit = MathToolkit()
tools = toolkit.get_tools()

for tool in tools:
    print(tool.name, "=>", tool.description)

# add => Add two numbers
# multiply => Multiply two numbers
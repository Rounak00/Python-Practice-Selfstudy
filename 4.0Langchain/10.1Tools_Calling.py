# Tool Binding -> LLM Undestand what are tools are there and what they can do 
# !pip install -q langchain-openai langchain-core requests

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
import requests
# tool create
@tool
def multiply(a: int, b: int) -> int:
  """Given 2 numbers a and b this tool returns their product"""
  return a * b

print(multiply.invoke({'a':3, 'b':4}))

# tool binding
llm = ChatOpenAI()
# llm.invoke('hi') give responses
# Bind tool with llm
llm_with_tools = llm.bind_tools([multiply])
llm_with_tools.invoke('Hi how are you') #Works properly

query = HumanMessage('can you multiply 3 with 1000')
messages = [query]
# print(message) -> [HumanMessage(content='can you multiply 3 with 1000', additional_kwargs={}, response_metadata={})]

result = llm_with_tools.invoke(messages)
messages.append(result)
# [HumanMessage(content='can you multiply 3 with 1000', additional_kwargs={}, response_metadata={}),
#  AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_RxxH1pPDylDECUwpRe7MXkJi', 'function': {'arguments': '{"a":3,"b":1000}', 'name': 'multiply'}, 'type': 'function'}], 'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 19, 'prompt_tokens': 63, 'total_tokens': 82, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'id': 'chatcmpl-BR8rS3DNc8cckcVLJMmBDxHENKUlV', 'finish_reason': 'tool_calls', 'logprobs': None}, id='run-8035ac83-7820-4681-b8c0-1d15aa24ca77-0', tool_calls=[{'name': 'multiply', 'args': {'a': 3, 'b': 1000}, 'id': 'call_RxxH1pPDylDECUwpRe7MXkJi', 'type': 'tool_call'}], usage_metadata={'input_tokens': 63, 'output_tokens': 19, 'total_tokens': 82, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})]

tool_result = multiply.invoke(result.tool_calls[0])#return a tol message -> ToolMessage(content='3000', name='multiply', tool_call_id='call_RxxH1pPDylDECUwpRe7MXkJi')

messages.append(tool_result) #Maintain coversation history

llm_with_tools.invoke(messages).content #The product of 3 and 1000 is 3000.

> Now assume we have a state for meassages to be added up one by one, and while loop for continous chatting now in while loop we call invoke everytime and this 
invoke() run the state from scratch so it will not get previous messages.

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
llm = ChatOpenAI()

def chat_node(state: ChatState):
    # take user query from state
    messages = state['messages']
    # send to llm
    response = llm.invoke(messages)
    # response store state
    return {'messages': [response]}
graph = StateGraph(ChatState)

# add nodes
graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)
chatbot = graph.compile()
initial_state = {
    'messages': [HumanMessage(content='What is the capital of india')]
}
chatbot.invoke(initial_state)['messages'][-1].content




So here comes the topic of persistance, we can store the state in RAM or DB (Best for production level is DB)
from langgraph.checkpoint.memory import MemorySaver
# ALl functions
checkpointer=MemorySaver()
# creation of graph
chatbot = graph.compile(checkpointer=checkpointer)
before sart while have a variable of thread_id=1l
and before invooke have config={"configurable":{"thread_id":thread_id}};
in invoke function also send config=config;



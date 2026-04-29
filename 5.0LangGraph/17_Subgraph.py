# Sub graph
# embedded and executed like a node inside a graph, mostly use in a multiagent system.
# There are two aways to make subgraph in langgraph ->
# 1. Invoke a graph from Node.
# 2. Add a Graph as a Node.
# For persistance in sibgraph we mostly give ir in parent only, langraph automaticaly checkpoint childrens.

# Practice code (States are isolated)
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

class SubState(TypedDict):

    input_text: str
    translated_text: str

subgraph_llm = ChatOpenAI(model='gpt-4o')
def translate_text(state: SubState):

    prompt = f"""
Translate the following text to Hindi.
Keep it natural and clear. Do not add extra content.

Text:
{state["input_text"]}
""".strip()
    
    translated_text = subgraph_llm.invoke(prompt).content

    return {'translated_text': translated_text}

subgraph_builder = StateGraph(SubState)

subgraph_builder.add_node('translate_text', translate_text)

subgraph_builder.add_edge(START, 'translate_text')
subgraph_builder.add_edge('translate_text', END)

subgraph = subgraph_builder.compile()


class ParentState(TypedDict):

    question: str
    answer_eng: str
    answer_hin: str
parent_llm = ChatOpenAI(model='gpt-4o-mini')/

def generate_answer(state: ParentState):
    answer = parent_llm.invoke(f"You are a helpful assistant. Answer clearly.\n\nQuestion: {state['question']}").content
    return {'answer_eng': answer}

def translate_answer(state: ParentState):
    # call the subgraph
    result = subgraph.invoke({'input_text': state['answer_eng']})
    return {'answer_hin': result['translated_text']}

parent_builder = StateGraph(ParentState)

parent_builder.add_node("answer", generate_answer)
parent_builder.add_node("translate", translate_answer)

parent_builder.add_edge(START, 'answer')
parent_builder.add_edge('answer', 'translate')
parent_builder.add_edge('translate', END)
graph = parent_builder.compile()

graph.invoke({'question': 'What is quantum physics'})



#  Subgraph where state are shared
#  use subgraph as node
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
class ParentState(TypedDict):

    question: str
    answer_eng: str
    answer_hin: str
    
parent_llm = ChatOpenAI(model='gpt-4o-mini')
subgraph_llm = ChatOpenAI(model='gpt-4o')

def translate_text(state: ParentState):

    prompt = f"""
Translate the following text to Hindi.
Keep it natural and clear. Do not add extra content.

Text:
{state["answer_eng"]}
""".strip()
    
    translated_text = subgraph_llm.invoke(prompt).content

    return {'answer_hin': translated_text}



def generate_answer(state: ParentState):
    answer = parent_llm.invoke(f"You are a helpful assistant. Answer clearly.\n\nQuestion: {state['question']}").content
    return {'answer_eng': answer}


subgraph_builder = StateGraph(ParentState)
subgraph_builder.add_node('translate_text', translate_text)
subgraph_builder.add_edge(START, 'translate_text')
subgraph_builder.add_edge('translate_text', END)
subgraph = subgraph_builder.compile()

parent_builder = StateGraph(ParentState)
parent_builder.add_node("answer", generate_answer)
parent_builder.add_node("translate", subgraph)
parent_builder.add_edge(START, 'answer')
parent_builder.add_edge('answer', 'translate')
parent_builder.add_edge('translate', END)

graph = parent_builder.compile()
graph.invoke({'question': 'What is quantum physics'})


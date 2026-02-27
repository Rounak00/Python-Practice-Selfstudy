> make a Squential workflow code

1. Create a venv and activate it then install langgraph, langchain, langchain_openai, dotenv
test code >  from langgraph.graph import StateGraph

creat e a simple BMI calculator Workflow > (non llm)
 
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
# Create the state
class BMIState(TypedDict):
    weight_kg: float
    height_m: float
    bmi: float
    category: str

# define your graph
graph = StateGraph(BMIState)
# add nodes
graph.add_node('calculate_bmi', calculate_bmi)
graph.add_node('label_bmi', label_bmi)
# add edges
graph.add_edge(START, 'calculate_bmi')
graph.add_edge('calculate_bmi', 'label_bmi')
graph.add_edge('label_bmi', END)
# compile graph
workflow = graph.compile()
# invoke/execute the graph
intial_state = {'weight_kg':80, 'height_m':1.73}
final_state = workflow.invoke(intial_state)
print(final_state)
{'weight_kg': 80, 'height_m': 1.73, 'bmi': 26.73, 'category': 'Overweight'}



> Now LLM Based workflow
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict
from dotenv import load_dotenv
load_dotenv()
model = ChatOpenAI()

# create a state
class LLMState(TypedDict):
    question: str
    answer: str



def llm_qa(state: LLMState) -> LLMState:
    # extract the question from state
    question = state['question']
    # form a prompt
    prompt = f'Answer the following question {question}'
    # ask that question to the LLM
    answer = model.invoke(prompt).content
    # update the answer in the state
    state['answer'] = answer
    return state


# create our graph
graph = StateGraph(LLMState)
# add nodes
graph.add_node('llm_qa', llm_qa)
# add edges
graph.add_edge(START, 'llm_qa')
graph.add_edge('llm_qa', END)

# compile
workflow = graph.compile()
# execute
intial_state = {'question': 'How far is moon from the earth?'}
final_state = workflow.invoke(intial_state)
print(final_state['answer'])

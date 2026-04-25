# Persistance is for -> save and restore a state of a workflow over time.
#  its like state is there p=but app forget its value after ENd node, also in seperate nodes 
#   a particular keys value and changed value need to save then we need persistance.

#  we can also handle fault tolerance using this  on a particular node.

# Checkpoint is the main thing for persistnace which will add in each superset of a graph [each node run korar age]
# Threads -> assign a thread id for a particular workfolwo each time invoke


from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
load_dotenv()
llm = ChatOpenAI()

class JokeState(TypedDict):
    topic: str
    joke: str
    explanation: str


def generate_explanation(state: JokeState):
    prompt = f'write an explanation for the joke - {state["joke"]}'
    response = llm.invoke(prompt).content
    return {'explanation': response}

def generate_joke(state: JokeState):

    prompt = f'generate a joke on the topic {state["topic"]}'
    response = llm.invoke(prompt).content
    return {'joke': response}


graph = StateGraph(JokeState)

graph.add_node('generate_joke', generate_joke)
graph.add_node('generate_explanation', generate_explanation)

graph.add_edge(START, 'generate_joke')
graph.add_edge('generate_joke', 'generate_explanation')
graph.add_edge('generate_explanation', END)

checkpointer = InMemorySaver()

workflow = graph.compile(checkpointer=checkpointer)
config1 = {"configurable": {"thread_id": "1"}}
workflow.invoke({'topic':'pizza'}, config=config1)


# To see the data -> 
# workflow.get_state(config1) => 
# StateSnapshot(values={'topic': 'pizza', 'joke': 'Why did the pizza go to the doctor? Because it was feeling a little saucy!', 'explanation': 'This joke plays on the double meaning of the word "saucy." In one sense, "saucy" can mean bold, impertinent, or sassy. But in the context of a pizza, "saucy" refers to the tomato sauce typically used as a base on pizzas. So when the pizza went to the doctor because it was feeling "saucy," it implies that the pizza was not feeling well due to too much sauce, rather than being bold or sassy. The humor comes from the unexpected twist on the word\'s meaning.'}, next=(), config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f06cc6e-93a2-6a08-8002-395e36be0f5e'}}, metadata={'source': 'loop', 'step': 2, 'parents': {}, 'thread_id': '1'}, created_at='2025-07-29T21:56:42.071296+00:00', parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f06cc6e-7a2f-60ea-8001-4ac26c539f8d'}}, tasks=(), interrupts=())

# list(workflow.get_state_history(config1)) => give value for each nodes
# [StateSnapshot(values={'topic': 'pizza', 'joke': 'Why did the pizza go to the doctor? Because it was feeling a little saucy!', 'explanation': 'This joke plays on the double meaning of the word "saucy." In one sense, "saucy" can mean bold, impertinent, or sassy. But in the context of a pizza, "saucy" refers to the tomato sauce typically used as a base on pizzas. So when the pizza went to the doctor because it was feeling "saucy," it implies that the pizza was not feeling well due to too much sauce, rather than being bold or sassy. The humor comes from the unexpected twist on the word\'s meaning.'}, next=(), config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f06cc6e-93a2-6a08-8002-395e36be0f5e'}}, metadata={'source': 'loop', 'step': 2, 'parents': {}, 'thread_id': '1'}, created_at='2025-07-29T21:56:42.071296+00:00', parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f06cc6e-7a2f-60ea-8001-4ac26c539f8d'}}, tasks=(), interrupts=()),
#  StateSnapshot(values={'topic': 'pizza', 'joke': 'Why did the pizza go to the doctor? Because it was feeling a little saucy!'}, next=('generate_explanation',), config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f06cc6e-7a2f-60ea-8001-4ac26c539f8d'}}, metadata={'source': 'loop', 'step': 1, 'parents': {}, 'thread_id': '1'}, created_at='2025-07-29T21:56:39.402519+00:00', parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f06cc6e-7232-6cb1-8000-f71609e6cec5'}}, tasks=(PregelTask(id='1f8e036d-b599-6074-0dac-c200937328d4', name='generate_explanation', path=('__pregel_pull', 'generate_explanation'), error=None, interrupts=(), state=None, result={'explanation': 'This joke plays on the double meaning of the word "saucy." In one sense, "saucy" can mean bold, impertinent, or sassy. But in the context of a pizza, "saucy" refers to the tomato sauce typically used as a base on pizzas. So when the pizza went to the doctor because it was feeling "saucy," it implies that the pizza was not feeling well due to too much sauce, rather than being bold or sassy. The humor comes from the unexpected twist on the word\'s meaning.'}),), interrupts=()),
#  StateSnapshot(values={'topic': 'pizza'}, next=('generate_joke',), config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f06cc6e-7232-6cb1-8000-f71609e6cec5'}}, metadata={'source': 'loop', 'step': 0, 'parents': {}, 'thread_id': '1'}, created_at='2025-07-29T21:56:38.565188+00:00', parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f06cc6e-7230-65a8-bfff-0a96c2fc4e11'}}, tasks=(PregelTask(id='dcd96e38-1f32-5ed6-9f44-fa2b22c193f0', name='generate_joke', path=('__pregel_pull', 'generate_joke'), error=None, interrupts=(), state=None, result={'joke': 'Why did the pizza go to the doctor? Because it was feeling a little saucy!'}),), interrupts=()),
#  StateSnapshot(values={}, next=('__start__',), config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f06cc6e-7230-65a8-bfff-0a96c2fc4e11'}}, metadata={'source': 'input', 'step': -1, 'parents': {}, 'thread_id': '1'}, created_at='2025-07-29T21:56:38.564189+00:00', parent_config=None, tasks=(PregelTask(id='2d4d902e-419f-6dff-1b83-385121fc185e', name='__start__', path=('__pregel_pull', '__start__'), error=None, interrupts=(), state=None, result={'topic': 'pizza'}),), interrupts=())]


# Advantage of persistance -> Timetravle, HITL, shortterm memory, Fault tolernace means failuer in  node.
# Timetravel go on a particular checkpoint and do again, now for that each checkpoint we also have checkpoint id and we need this
-> workflow.get_state({"configurable": {"thread_id": "1", "checkpoint_id": "1f06cc6e-7232-6cb1-8000-f71609e6cec5"}})
   workflow.invoke(None, {"configurable": {"thread_id": "1", "checkpoint_id": "1f06cc6e-7232-6cb1-8000-f71609e6cec5"}})
#    new content added on that same array of checkpointsof the thread

# Resume from a particular state -> final_state = graph.invoke(None, config={"configurable": {"thread_id": 'thread-1'}})




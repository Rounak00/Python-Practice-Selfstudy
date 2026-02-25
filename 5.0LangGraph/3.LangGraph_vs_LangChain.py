Agentic AI Tools  -> CrewAI, Microsoft Autogen, varcel AI SDK, Langgraph

Workflow -> Done by human
Agent -> run in a particular workflow and each time workflow can be different

Challenges in Langchain -> 
   1. Control flow complexity -> Loop logic langchain dont have, jump and conditional branching all also dont have
   2. Handlig State -> Data in the entire workflow, that will evolpo during execution of workflow
   3. Event Driven execution -> Wait in a node and then trigger on a event
   4. Fault tollerance -> recover fault and then run (small and big fault) [retry, recovery, resume]
   5. Human in the loop -> pause for human interaction
   > challenge 3,4,5 connected with statefull
   6. Nested Workflow -> ctreate sub graphs that helps for reusability, multiagent feature
   7. Observability -> monitor, debug and understand how workflow going (Langsmith -> can only monitor langchain/langGraph not glue code.)

LanGraph Definition -> 
LangGraph is a framework for building stateful, multi-step AI workflows where an LLM can reason, decide, and call tools using a graph structure instead of a simple chain.

Now let me make it crystal clear:

In LangChain → you mostly build linear chains (A → B → C)

In LangGraph → you build a graph with:
Nodes (steps like LLM call, tool call, function)
Edges (how control moves between steps)
State (shared memory across steps)

That means:
👉 It supports loops
👉 It supports conditional branching
👉 It supports retries
👉 It supports multi-agent systems
👉 It supports long-running workflows

This is why people use it for agentic AI systems.

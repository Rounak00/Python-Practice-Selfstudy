# Langsmith traces -> 
Input Output, Cost, All the immediate steps, latency, tokens usage, error, tags, metadata, Feedback .

# mostly env things to add in project for langsmith trace -> 
#                         LANGSMITH_TRACING, LANGSMITH_ENDPOINT, LANGSMITH_API_KEY, LANGSMITH_PROJECT


# Create a accoutn in langsmith -> create api key -> setup langsmith in app ->  in langsmith tracing project we can see our projects

# RAG can have 2 type of errors Retriever erros and generator error that we can sole using Langsmith
# @traceable() decorators give each function a name, and get those as a difeferent trace in langsmith.
#              basically use to trace any normal python fucntion as well. we can add tags & Metadata also.



# LangSmith with Langgraph -> 
# each node become a run inside a trace, each node run inside trace, -> can see path taken
# based on langgraph if we want we can keep all traces based on threads. 
#             for this the CONFIG variable that is  the code we have to update that a lil basically with metadata and run_name

# Langsmith is not only for observability but for 
#     monitoring and alarming, Evaluation(as llm non diterministic), Prompt experimentation, Dataset Creation and anotation,
#     user feedback intigration, collaboration
  
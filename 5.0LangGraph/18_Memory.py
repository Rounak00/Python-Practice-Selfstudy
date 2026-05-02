# Memory -> without it we cant make a Agentic AI
# A LLM  inference  is a parmeterized math function. 
# y=f theta (x) here x is token or propmpt, f is a complex func and theta is billion of parmas
# y is output tokens but it depends on theta and x, now here theta is fixed but x is not


# Now this math function is stateless, means output depends on current input and not anything that happened before.
# like assking a name using a LLM is a a operation and then ask whatbis my name is a another function and hence both are stateless by nature
# so LLM dont have any intrinsic memory ie, past conversations not save.
# The memory thing is get by implemnt by our own.

# Context window -> the amount of data that llm can read and remeber at one time before answering,
#  modern llms have 128k token assumption 200 page pdf



# In context learning -> in large data llm try to search patterns and make a parametric models , now for answer prompts it may use this parametric data model but can also use prompt to answer
# so from prompt llm can generate answer as well


# NOw in LLM we have short term and longterm memory (STM & LTM)
# In LLM concept context in prompt its actaully temporary now its also known as Short Term Memory.
#        So basically in Chatgpt each conversation have a STM. conversations also can be called as thread so STM is a Thread Scope.
#   Issues in STM -> Its fragile, Thread scope, context window issue ie context is too big(for solving it we use trimming+Summarizations+Hybrid),  



# Now we need new memory as STM cant solve everything, special information can store for a longer time, store only usefu;; things not all chat
#  this type of memory is Long term memory (LTM)
# Three typs of LTM in LLm -> 
# 1. Episodic Memory : past events and experiences
# 2. Semantic Memory : Fact, Knowledge and stable info (This is most important) 
# 3. Procedural Memory : Strategies, Rules, Learn , Behaviours (How need to do things)
# Now LTM have 4 steps -> 
    # 1. creation - its like anything that can be a part of LTM
    # 2. Storage - store with meta data and tags
    # 3.Retrival - retrieve of the data, selective data
    # 4. Injecttion - LTM direct interaction not happened so LTM be a part of  STM first then model see it as more tokens

# Mem0, Super memmory, LangMem are LTM

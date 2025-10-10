# Retrieval Augmented Generation 
# Problems: 
# 1. Private Data
# 2. Recent data
# 3. Helosination

# we can solve those using fine tuning
# Finetuning -> Supervised finetuning, Unsupervised Finetuning
# now for fine tuning its expensieve and need good ai engineers and hard to do for a notmal person
# So we still solve it using in context learing -> Based on the some example prompts the model learns

# Operations in RAG 
# 1. Indexing(Creation of knowledge base) -> Doc Ingestion - Text Chunking - Embedding Generations - Stroe in vector store
# 2. Retriving (Search in knowledgebase) -> Query to Vector and then search in vector perform ranking 
# 3. Augmentation (Context, Query merge and make a prompt)
# 4. Generation (Prompt send to LLM) 

# Cheaper and simpler alternative than fine tuning
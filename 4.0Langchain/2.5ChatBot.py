# chatbot 
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
load_dotenv()

model = ChatOpenAI()
while True:
    user_input = input('You: ')
    if user_input == 'exit':
        break
    result = model.invoke(chat_history)
    print("AI: ",result.content)

# State the previous messages
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI()

chat_history = [
    SystemMessage(content='You are a helpful AI assistant')
]

while True:
    user_input = input('You: ')
    chat_history.append(HumanMessage(content=user_input))
    if user_input == 'exit':
        break
    result = model.invoke(chat_history)
    chat_history.append(AIMessage(content=result.content))
    print("AI: ",result.content)

print(chat_history)


# Message level chatbot  used this in previous code
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

model = ChatOpenAI()
messages=[
    SystemMessage(content='You are a helpful assistant'),
    HumanMessage(content='Tell me about LangChain')
]

result = model.invoke(messages)
messages.append(AIMessage(content=result.content))
print(messages)


# List message (Chat Prompt template)
# /chat_prompt_template
from langchain_core.prompts import ChatPromptTemplate

chat_template = ChatPromptTemplate([ # can use SeystemMessage and HumanMessage class as well
    ('system', 'You are a helpful {domain} expert'),
    ('human', 'Explain in simple terms, what is {topic}')
])

prompt = chat_template.invoke({'domain':'cricket','topic':'Dusra'})

print(prompt)

# Message Placeholder -> use to make chatPrompTemplate have the history of chat
# chat history ->
# HumanMessage(content="I want to request a refund for my order #12345.")
# AIMessage(content="Your refund request for order #12345 has been initiated. It will be processed in 3-5 business days.")
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# chat template
chat_template = ChatPromptTemplate([
    ('system','You are a helpful customer support agent'),
    MessagesPlaceholder(variable_name='chat_history'),
    ('human','{query}')
])

chat_history = []
# load chat history
with open('chat_history.txt') as f:
    chat_history.extend(f.readlines())

print(chat_history)

# create prompt
prompt = chat_template.invoke({'chat_history':chat_history, 'query':'Where is my refund'})

print(prompt)
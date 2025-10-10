# prompts are the things thatwe send as in invoke()
#  text and multimodel prompts both are there
# We mostly use text prompts 

# static and dynamic prompt both are there and static prompts are not use much
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI()

# detailed way
template2 = PromptTemplate(
    template='Greet this person in 5 languages. The name of the person is {name}',
    input_variables=['name']
)

# fill the values of the placeholders
prompt = template2.invoke({'name':'nitish'})

result = model.invoke(prompt)

print(result.content)



# sowe can use a template for a dynamic prompt 
# template generator 
from langchain_core.prompts import PromptTemplate

# template
template = PromptTemplate(
    template="""
Please summarize the research paper titled "{paper_input}" with the following specifications:
Explanation Style: {style_input}  
Explanation Length: {length_input}  
1. Mathematical Details:  
   - Include relevant mathematical equations if present in the paper.  
   - Explain the mathematical concepts using simple, intuitive code snippets where applicable.  
2. Analogies:  
   - Use relatable analogies to simplify complex ideas.  
If certain information is not available in the paper, respond with: "Insufficient information available" instead of guessing.  
Ensure the summary is clear, accurate, and aligned with the provided style and length.
""",
input_variables=['paper_input', 'style_input','length_input'],
validate_template=True
)

template.save('template.json')
# template
{
    "name": null,
    "input_variables": [
        "length_input",
        "paper_input",
        "style_input"
    ],
    "optional_variables": [],
    "output_parser": null,
    "partial_variables": {},
    "metadata": null,
    "tags": null,
    "template": "\nPlease summarize the research paper titled \"{paper_input}\" with the following specifications:\nExplanation Style: {style_input}  \nExplanation Length: {length_input}  \n1. Mathematical Details:  \n   - Include relevant mathematical equations if present in the paper.  \n   - Explain the mathematical concepts using simple, intuitive code snippets where applicable.  \n2. Analogies:  \n   - Use relatable analogies to simplify complex ideas.  \nIf certain information is not available in the paper, respond with: \"Insufficient information available\" instead of guessing.  \nEnsure the summary is clear, accurate, and aligned with the provided style and length.\n",
    "template_format": "f-string",
    "validate_template": true,
    "_type": "prompt"
}

# fill the values of the placeholders
prompt = template2.invoke({'name':'nitish'})

result = model.invoke(prompt)

print(result.content)

# useing the template
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import PromptTemplate,load_prompt

load_dotenv()
model = ChatOpenAI()

st.header('Reasearch Tool')

paper_input = st.selectbox( "Select Research Paper Name", ["Attention Is All You Need", "BERT: Pre-training of Deep Bidirectional Transformers", "GPT-3: Language Models are Few-Shot Learners", "Diffusion Models Beat GANs on Image Synthesis"] )

style_input = st.selectbox( "Select Explanation Style", ["Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical"] ) 

length_input = st.selectbox( "Select Explanation Length", ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explanation)"] )

template = load_prompt('template.json')



if st.button('Summarize'):
    chain = template | model
    result = chain.invoke({
        'paper_input':paper_input,
        'style_input':style_input,
        'length_input':length_input
    })
    st.write(result.content)


    
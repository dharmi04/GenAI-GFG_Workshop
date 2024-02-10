# Import the required modules
from langchain_google_genai import GoogleGenerativeAI  # Use to access the Google Generative AI
from langchain import PromptTemplate  # Use to create a prompt template
from langchain.chains import LLMChain  # Use to create a chain of LLMs
from langchain.chains import SequentialChain  # Use to create a chain (Sequential) of LLMs


import streamlit as st  # Use to create the web app


import os
import dotenv


dotenv.load_dotenv()


# the icon and the title of the web app
st.set_page_config(page_title="On That Day...", page_icon="🏰")




# streamlit framework
st.title('On That Day...')
input_text = st.text_input("Name a celebrity")


# Gemini LLMS
google_api_key = "AIzaSyB-E1yplhCxbcuYIrO38AGW5DTWHFveK3A"  # Google API Key
llm = GoogleGenerativeAI(temperature=0.8, google_api_key=google_api_key, model="gemini-pro")  # Initialize the Gemini LLM


# First Prompt Templates
first_input_prompt = PromptTemplate(
   input_variables=['name'],  # Input variables for creating the prompt template (Here name is the input variable)
   template="Tell me about celebrity {name}"
)


# Chain of LLMs
chain = LLMChain(  # First Chain Which uses the first prompt template to find about the person
   llm=llm,  # Pass the LLM (For our case it is Gemini LLM)
   prompt=first_input_prompt,  # Pass the prompt template
   verbose=True,  # Use verbose to print the output
   output_key='person'  # Output key to store the output of the LLM (person is the output key for the first chain so person will contain information about the person)
)


# Second Prompt Templates
second_input_prompt = PromptTemplate(  # Second Prompt Template
   input_variables=['person'],  # Input variables for creating the prompt template (Here person is the input variable)
   template="when was {person} born"  # Template for the prompt
)


# Chain of LLMs
chain2 = LLMChain(  # Second Chain Which uses the second prompt template to find the person's DOB
   llm=llm, prompt=second_input_prompt, verbose=True, output_key='dob'
)


# Prompt Templates
third_input_prompt = PromptTemplate( # Third Prompt Template
   input_variables=['dob'], # Input variables for creating the prompt template (Here dob is the input variable)
   template="Mention 5 major events happened around {dob} in the world" # Template for the prompt
)


chain3 = LLMChain(llm=llm, prompt=third_input_prompt, verbose=True, output_key='description') # Third Chain Which uses the third prompt template to find the person's DOB


parent_chain = SequentialChain( # Parent Chain Which uses the first, second and third chain to find the person's details
   chains=[chain, chain2, chain3], input_variables=['name'], # There is only one input variable which is name
     output_variables=['person', 'dob', 'description'],
   verbose=True
)


if input_text:
   result = parent_chain({'name': input_text})
   # st.write(result)
  
   # st expended the text box
   with st.expander("Name"):
       st.write(result['name'])


   with st.expander("Details"):
       st.write(result['person'])


   with st.expander("Date of Birth"):
       st.write(result['dob'])


   with st.expander("Around his DOM in the world"):
       st.write(result['description'])
      
   st.write('Data Fetched Successfully')

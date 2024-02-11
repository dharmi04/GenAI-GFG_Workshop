import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.llms import Gemini
from llama_index.embeddings import GeminiEmbedding
from llama_index import SimpleDirectoryReader


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate  # Fix import


st.set_page_config(page_title="Chat with Document", page_icon="📚")


@st.cache_resource(show_spinner=False)
def load_data():
   with st.spinner(text="Loading and indexing the Documents – hang tight! This should take 1-2 minutes."):

       llm = Gemini(api_key="AIzaSyB-E1yplhCxbcuYIrO38AGW5DTWHFveK3A")
       llm = Gemini(api_key="AIzaSyB-E1yplhCxbcuYIrO38AGW5DTWHFveK3A")
       embed_model = GeminiEmbedding(api_key="AIzaSyB-E1yplhCxbcuYIrO38AGW5DTWHFveK3A")  # Fix typo
       service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)  # Fix variable name


       reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
       documents = reader.load_data()
       index = VectorStoreIndex.from_documents(documents=documents, service_context=service_context)
       return index

    
index = load_data()


if "chat_engine" not in st.session_state.keys():
   st.session_state.chat_engine = index.as_chat_engine(chat_mode="context", verbose=True)
   llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key="AIzaSyB-E1yplhCxbcuYIrO38AGW5DTWHFveK3A", temperature=0.1)
   st.session_state.langchain_chat_engine = ConversationChain(llm=llm, verbose=True, memory=ConversationBufferMemory())


st.title("Chat With Document")


if "messages" not in st.session_state.keys():
   st.session_state.messages = [
       {"role": "assistant", "content": "Ask me questions ..."}
   ]
prompt = st.chat_input("Your question")


if prompt: 
   st.session_state.messages.append({"role": "user", "content": prompt})


for message in st.session_state.messages:
   with st.chat_message(message["role"]):
       st.write(message["content"])

if st.session_state.messages and st.session_state.messages[-1]["role"] != "assistant":  
   with st.spinner("Thinking..."):
       response = st.session_state.chat_engine.chat(prompt)
       response = response.response


       template = ChatPromptTemplate.from_messages([
               ("system", "Act as the AI Bot Which Give the Answer of the Question asked by the User. Using the Context which will be provided. Do not give the answer which is not relevant to the context. If the question is irrelevant with respect to the context then, kindly suggest to contact developer. Do not give incorrect answer. Context:  `{response}`"),
               ("human", st.session_state.messages[-1]["content"]),
               ("ai", st.session_state.messages[-2]["content"]),
               ("human", "{user_input}"),
           ]) 
       messages1 = template.format_messages(
               user_input=prompt,
               response=response
           )
       response = st.session_state.langchain_chat_engine.predict(input=messages1)
       response = response.replace("AIMessage(content='", "").replace("')", "")
       st.write(response)
       message = {"role": "assistant", "content": response}
       st.session_state.messages.append(message)
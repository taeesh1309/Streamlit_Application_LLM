
import streamlit as st

import asyncio

from services.llm import  create_conversation_starter
from helpers.util import run_conversation

import asyncio

from helpers.util import run_conversation
from services.prompts import (
    general_ducky_prompt, 
    review_code_prompt, 
    modify_code_prompt, 
    debug_code_prompt, 
)

async def converse_with_llm_async(prompt):
    messages = create_conversation_starter(prompt)
    response = await run_conversation(messages, st.empty())
    return response[-1]["content"]



def converse_with_llm(prompt):
    return asyncio.run(converse_with_llm_async(prompt))



st.set_page_config(page_title="Generate Code", page_icon="💻", layout="wide")


st.sidebar.title("Hello there 👋")
feature = st.sidebar.selectbox("What kind of Task do you intend on doing?", ["Review Code", "Debug Code", "Modify Code"])

if feature == "Review Code":
    st.header("Review Code")
    code = st.text_area("Enter your code here which you want to review", height=300)
    if st.button("Review Code"):
        review_info = converse_with_llm(review_code_prompt(code))
        review_info = review_info.split("\n", 1)[0]
        st.write(review_info)

elif feature == "Debug Code":
    st.header("Debug Code")
    code = st.text_area("Enter your code here which you want to debug", height=250)
    error_string = st.text_input("Enter the error string (optional)")
    if st.button("Debug Code"):
        debug_info = converse_with_llm(debug_code_prompt(code, error_string))
        debug_info = debug_info.split("\n", 1)[0]
        st.write(debug_info)

elif feature == "Modify Code":
    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    st.header("Modify your code below 🦆")
    st.write("Let's collaborate on adjusting your code! Share your requirements, and I'll guide you through the process.")

    if "messages" not in st.session_state:
        initial_messages = [{"role": "system",
                            "content": general_ducky_prompt()}]
        st.session_state.messages = initial_messages


    for message in [m for m in st.session_state.messages if m["role"] != "system"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    async def chat(messages):
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            messages = await run_conversation(messages, message_placeholder)
            st.session_state.messages = messages
        return messages


    if prompt := st.chat_input("Enter instruction and code which you want to modify..."):
        st.session_state.messages.append({"role": "user", "content": modify_code_prompt(prompt)})
        asyncio.run(chat(st.session_state.messages)) 


# Reset functionality
if st.sidebar.button("Reset"):
    st.experimental_rerun()

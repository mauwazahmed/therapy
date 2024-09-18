import streamlit as st
from openai import OpenAI

system_prompt = ''

# Define the system prompt
with open('therapy_prompt2.txt','r', encoding = 'utf-8') as f:
    system_prompt = str(f.read())


# Sidebar for API key input
with st.sidebar:
    user_key = st.text_input("Add OpenAI API Key", type="password")

if user_key:
    client = OpenAI(api_key = user_key)
    
    st.title("AI Therapist")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": system_prompt},
            {"role": "assistant", "content": "Hello Sir/Ma'am, I am pleased to be at your service. How are you feeling today?"}
        ]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] != 'system':
                st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("Type your query here"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response from OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
        ).choices[0].message.content

        # Display response
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
else:
    st.warning("Please enter your OpenAI API key in the sidebar.")

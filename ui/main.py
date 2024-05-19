import streamlit as st

from services.rasa_api import get_rasa_response
from services.chat_histories import save_chat_history, load_chat_history


st.title("Courssistant")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

# Initialize or load chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# Sidebar with a button to delete chat history
with st.sidebar:
    if st.button("Delete Chat History"):
        st.session_state.messages = []
        save_chat_history([])

# Display chat messages in the sidebar
with st.sidebar:
    st.header("Chat with Rasa Bot")
    
    chat_container = st.container()  # Create a container for chat messages

    # Display chat messages in reverse order (newest at the bottom)
    with chat_container:
        for i, message in enumerate(st.session_state.messages):
            avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    # User input in the sidebar
    with st.form(key='chat_form', clear_on_submit=True):
        user_input = st.text_input("How can I help?", key="user_input")
        submit_button = st.form_submit_button(label="Send")

    if submit_button and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display the user's message
        with chat_container:
            with st.chat_message("user", avatar=USER_AVATAR):
                st.markdown(user_input)
    

        responses = get_rasa_response(user_input)
        full_response = ""
        for response in responses:
            full_response += response.get("text", "")
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Display Rasa's response
        with chat_container:
            with st.chat_message("assistant", avatar=BOT_AVATAR):
                st.markdown(full_response)

        # Save chat history after each interaction
        save_chat_history(st.session_state.messages)

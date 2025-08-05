import streamlit as st

from models import Conversation, Message
from services import MessageSubmissionService

st.session_state.setdefault("conversation", Conversation())


def handle_chat_input_submit():
    user_message = Message(
        role="user", type="text", content=st.session_state["chat_input"]
    )

    with conversation.container():
        with st.chat_message(user_message.role):
            st.write(user_message.content)

        with st.spinner(text="Processing...", show_time=True):
            assistant_message = MessageSubmissionService(
                st.session_state.conversation
            ).send_message(user_message)
            st.session_state.conversation.messages.append(user_message)
            st.session_state.conversation.messages.append(assistant_message)


## UI COMPONENTS ##

with st.sidebar:
    st.logo(
        "https://cdn.prod.website-files.com/66cf2bfc3ed15b02da0ca770/66d07240057721394308addd_Logo%20(1).svg",
        size="large",
    )
    st.title("Support Conversation Demo")
    st.write(
        """
        This is a conversation use case that demonstrates HITL capabilities using CrewAI.

        Imagine this in the hands of Customer Support employees. It boots their productivity by
        allowing them to interact with a series of agents capable of fetching and propagating side-effects
        consistently on ticket systems (**Linear** in this case).

        **See that despite the usage of Agents/LLMs here, all the control is in the hands of the user.**
        """
    )
    st.divider()
    st.write(
        "If applications like this interest you, please find out more about us at https://crewai.com/."
    )
    st.link_button(
        "**Sign up for a Free Trial**", "https://app.crewai.com/", type="primary"
    )


with st.container():
    st.title("Conversation")
    conversation = st.container()

with st._bottom:
    st.chat_input(
        key="chat_input",
        placeholder="Interact with your Support Agent here",
        on_submit=handle_chat_input_submit,
    )

for message in st.session_state.conversation.messages:
    with conversation.container():
        with st.chat_message(message.role):
            st.write(message.content)

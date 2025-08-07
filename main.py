import streamlit as st

from models import Conversation, Message
from services import MessageSubmissionService

st.session_state.setdefault("conversation", Conversation())


def _handle_chat_input_submit():
    user_message = Message(
        role="user", type="text", content=st.session_state["chat_input"]
    )
    _process_user_message(user_message)


def _submit_cta_response(confirm: bool, idx: int):
    done_key = f"cta_done_{idx}"
    comment_key = f"cta_comment_{idx}"

    st.session_state[done_key] = True
    yes_or_no = "Yes" if confirm else "No"
    comments = st.session_state.get(comment_key, "").strip()

    user_message = Message(
        role="user",
        type="text",
        content=f"{yes_or_no}. {comments}",
    )
    _process_user_message(user_message)


def _process_user_message(user_message: Message):
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


@st.fragment
def _render_message(message: Message):
    with st.chat_message(message.role):
        match message.type:
            case "text":
                st.write(message.content)
            case "cta_confirmation":
                st.write(message.content)

                with st.form(f"cta_form_{i}", clear_on_submit=False):
                    already_interacted = st.session_state.get(f"cta_done_{i}", False)

                    choice = st.radio(
                        "Please confirm",
                        options=["Yes", "No"],
                        index=1,
                        key=f"cta_choice_{i}",
                        horizontal=True,
                        disabled=already_interacted,
                    )

                    comment_key = f"cta_comment_{i}"
                    st.text_area(
                        "Additional comments (optional)",
                        key=comment_key,
                        placeholder="Add any details you think are important...",
                        height=80,
                        disabled=already_interacted,
                    )

                    submitted = st.form_submit_button(
                        "Submit",
                        use_container_width=True,
                        disabled=already_interacted,
                    )
                    if submitted:
                        _submit_cta_response(confirm=(choice == "Yes"), idx=i)
                        st.rerun()


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
        on_submit=_handle_chat_input_submit,
    )

for i, message in enumerate(st.session_state.conversation.messages):
    with conversation.container():
        _render_message(message)

import streamlit as st

from haystack.dataclasses import ChatMessage
from llm import setup_pipeline,chat_with_ai,process_pdf


# Page config
st.set_page_config(page_title="Course Scheduler Assistant", page_icon="📚", layout="wide")

# Initialize Streamlit session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'conversation_started' not in st.session_state:
    st.session_state.conversation_started = False
if "latest_syllabus" not in st.session_state:
    st.session_state.latest_syllabus = None
if "pipe" not in st.session_state:
    st.session_state.pipe = setup_pipeline()


# Streamlit UI
st.title("Course Scheduler Assistant")

#Reset Conversation
if st.sidebar.button("Reset Conversation"):
    st.session_state.messages = []
    st.session_state.latest_syllabus = None
    st.session_state.conversation_started = False
    st.session_state.pdf_content = None
    if 'pdf_processed' in st.session_state:
        del st.session_state.pdf_processed
    st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message.role):
        st.markdown(message.content)

if not st.session_state.conversation_started:
    st.session_state.conversation_started = True
    initial_message = ChatMessage.from_assistant("Hello! I'm here to help you create a Course Schedule. Please upload a PDF file of your current schedule, or let me know if you'd like to start from scratch.")
    st.session_state.messages.append(initial_message)
    with st.chat_message("assistant"):
        st.markdown(initial_message.content)

uploaded_file = st.file_uploader("Upload Course Schedule PDF", type="pdf")
if uploaded_file is not None and 'pdf_processed' not in st.session_state:
    pdf_content = process_pdf(uploaded_file)
    st.session_state.pdf_content = pdf_content
    st.session_state.pdf_processed = True
    pdf_message = ChatMessage.from_assistant("I've successfully processed the uploaded PDF. Let me analyze its contents and we can discuss how to optimize your course schedule.")
    st.session_state.messages.append(pdf_message)
    with st.chat_message("assistant"):
        st.markdown(pdf_message.content)


if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append(ChatMessage.from_user(prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        full_response = chat_with_ai(st.session_state.messages, st.session_state.pipe, st.session_state.get('pdf_content'))
        st.markdown(full_response)
    assistant_message = ChatMessage.from_assistant(full_response)
    st.session_state.messages.append(assistant_message)

    # Check if the response contains a final course schedule
    if "[FINAL_COURSE_SCHEDULE]" in full_response:
        st.session_state.latest_schedule = full_response.split("[FINAL_COURSE_SCHEDULE]")[1].strip()
        st.success("Course schedule generated successfully!")


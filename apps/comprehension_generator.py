import streamlit as st
from helper.comprehension_gpt import *
from helper.document_processor_gpt import extract_summarized_document, save_uploaded_file

def comprehension_generator():
    st.title("Text Based Question Generator")

    # Initialize session state variables
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ''
    if 'grade_level' not in st.session_state:
        st.session_state.grade_level = ''
    if 'comprehension_no_of_questions' not in st.session_state:
        st.session_state.comprehension_no_of_questions = 5
    if 'comprehension_topic_or_text' not in st.session_state:
        st.session_state.comprehension_topic_or_text = ''
    if 'comprehension_response' not in st.session_state:
        st.session_state.comprehension_response = ''
    if 'comprehension_input_attempted' not in st.session_state:
        st.session_state.comprehension_input_attempted = False

    # Input fields
    api_key = st.text_input("Enter your API key", type='password', value=st.session_state.api_key)
    grade_level = st.text_input("Enter Grade Level:", value=st.session_state.grade_level)
    comprehension_topic_or_text = st.text_area("Enter Topic or Text:", value=st.session_state.comprehension_topic_or_text)
    comprehension_no_of_questions = st.number_input("Enter Number of Questions:", min_value=1, value=st.session_state.comprehension_no_of_questions)

    st.session_state.api_key = api_key
    st.session_state.grade_level = grade_level
    st.session_state.comprehension_topic_or_text = comprehension_topic_or_text
    st.session_state.comprehension_no_of_questions = comprehension_no_of_questions

    # File upload for images, DOCX, and PDF
    uploaded_file = st.file_uploader("Upload an image, DOCX, or PDF file", type=["png", "jpg", "jpeg", "docx", "pdf"])
    filepath = ''
    if uploaded_file:
        filepath = save_uploaded_file(uploaded_file)

    # Generate Comprehension button
    if st.button('Generate Comprehension'):
        file_content = extract_summarized_document(filepath, api_key, 'comprehension')
        st.session_state.comprehension_input_attempted = True
        if api_key and grade_level and comprehension_topic_or_text and comprehension_no_of_questions:
            try:
                st.session_state.comprehension_response = generate_comprehension_response(
                    api_key, 
                    grade_level, 
                    comprehension_no_of_questions, 
                    comprehension_topic_or_text+file_content
                    )
            except Exception as e:
                st.error(f'An error occurred: {e}')
        else:
            st.session_state.comprehension_response = None

    # Show error message only if input has been attempted and data not fetched
    if st.session_state.comprehension_input_attempted and not st.session_state.comprehension_response:
        st.error("Please fill in all the fields correctly.")

    if st.session_state.comprehension_response:
        st.subheader('Generated Comprehension:')
        st.markdown(f"```{st.session_state.comprehension_response}```", unsafe_allow_html=True)
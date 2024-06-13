import streamlit as st
from helper.worksheet_gpt import generate_worksheet_response
from helper.document_processor_gpt import extract_summarized_document, save_uploaded_file

def worksheet_generator():
    st.title("Worksheet Generator")

    # Initialize session state variables
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ''
    if 'grade_level' not in st.session_state:
        st.session_state.grade_level = ''
    if 'worksheet_topic_or_text' not in st.session_state:
        st.session_state.worksheet_topic_or_text = ''
    if 'worksheet_response' not in st.session_state:
        st.session_state.worksheet_response = ''
    if 'worksheet_input_attempted' not in st.session_state:
        st.session_state.worksheet_input_attempted = False

    # Input fields
    api_key = st.text_input("Enter your API key", type='password', value=st.session_state.api_key)
    grade_level = st.text_input("Enter Grade Level:", value=st.session_state.grade_level)
    worksheet_topic_or_text = st.text_area("Enter Topic or Text:", value=st.session_state.worksheet_topic_or_text)

    st.session_state.api_key = api_key
    st.session_state.grade_level = grade_level
    st.session_state.worksheet_topic_or_text = worksheet_topic_or_text
        
    # File upload for images, DOCX, and PDF
    uploaded_file = st.file_uploader("Upload an image, DOCX, or PDF file", type=["png", "jpg", "jpeg", "docx", "pdf"])
    filepath = ''
    if uploaded_file:
        filepath = save_uploaded_file(uploaded_file)

    # Generate Worksheet button
    if st.button('Generate Worksheet'):
        file_content = extract_summarized_document(filepath, api_key, 'worksheet')
        st.session_state.worksheet_input_attempted = True
        if api_key and (grade_level or file_content!='') and worksheet_topic_or_text:
            try:
                st.session_state.worksheet_response = generate_worksheet_response(api_key, grade_level, worksheet_topic_or_text+file_content)
            except Exception as e:
                st.error(f'An error occurred: {e}')
        else:
            st.session_state.worksheet_response = None

    # Show error message only if input has been attempted and data not fetched
    if st.session_state.worksheet_input_attempted and not st.session_state.worksheet_response:
        st.error("Please fill in all the fields correctly.")

    if st.session_state.worksheet_response:
        st.subheader('Generated Worksheet:')
        st.markdown(f"```{st.session_state.worksheet_response}```", unsafe_allow_html=True)
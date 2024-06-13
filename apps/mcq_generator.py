import streamlit as st
from helper.mcq_gpt import generate_mcq_response, parse_mcq_prompt
from helper.document_processor_gpt import extract_summarized_document, save_uploaded_file

def mcq_generator():
    st.title("MCQ Generator")

    # Initialize session state variables
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ''
    if 'mcq_passage' not in st.session_state:
        st.session_state.mcq_passage = ''
    if 'mcq_no_of_questions' not in st.session_state:
        st.session_state.mcq_no_of_questions = 5
    if 'mcq_response' not in st.session_state:
        st.session_state.mcq_response = ''
    if 'mcq_input_attempted' not in st.session_state:
        st.session_state.mcq_input_attempted = False
    if 'mcq_submitted' not in st.session_state:
        st.session_state.mcq_submitted = False
    if 'mcq_answers' not in st.session_state:
        st.session_state.mcq_answers = {}
    if 'mcq_correct_answers' not in st.session_state:
        st.session_state.mcq_correct_answers = {}

    # Input fields
    api_key = st.text_input("Enter your API key", type='password', value=st.session_state.api_key)
    mcq_passage = st.text_area("Enter Topic or Text:", value=st.session_state.mcq_passage)
    mcq_no_of_questions = st.number_input("Enter Number of Questions:", min_value=1, value=st.session_state.mcq_no_of_questions)

    st.session_state.api_key = api_key
    st.session_state.mcq_passage = mcq_passage
    st.session_state.mcq_no_of_questions = mcq_no_of_questions
    
    # File upload for images, DOCX, and PDF
    uploaded_file = st.file_uploader("Upload an image, DOCX, or PDF file", type=["png", "jpg", "jpeg", "docx", "pdf"])
    filepath = ''
    if uploaded_file:
        filepath = save_uploaded_file(uploaded_file)

    # Generate MCQs button
    if st.button('Generate MCQs'):
        file_content = extract_summarized_document(filepath, api_key, 'mcq')
        st.session_state.mcq_input_attempted = True
        if api_key and (mcq_passage or file_content!='') and mcq_no_of_questions:
            try:
                st.session_state.mcq_response = generate_mcq_response(api_key, mcq_passage+file_content, mcq_no_of_questions)
                st.session_state.mcq_submitted = False  # Reset submission state
            except Exception as e:
                st.error(f'An error occurred: {e}')
        else:
            st.session_state.mcq_response = None

    # Show error message only if input has been attempted and data not fetched
    if st.session_state.mcq_input_attempted and not st.session_state.mcq_response:
        st.error("Please fill in all the fields correctly.")

    mapping = {
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3
    }
    
    if st.session_state.mcq_response:
        st.subheader('Generated MCQs:')
        questions, choices, answers = parse_mcq_prompt(st.session_state.mcq_response)

        for idx, question in enumerate(questions):
            st.write(f"Q{idx + 1}: {question}")

            # Use the session state to set the initial selected value
            if question not in st.session_state.mcq_answers:
                st.session_state.mcq_answers[question] = None

            # Determine the index of the previously selected answer, if it exists
            selected_index = None
            if st.session_state.mcq_answers[question]:
                try:
                    selected_index = choices[idx].index(st.session_state.mcq_answers[question])
                except ValueError:
                    selected_index = None

            user_answer = st.radio(
                "Select your answer:", choices[idx], 
                key=f"{question}_options",
                index=selected_index
            )

            # Update session state with the selected answer immediately
            st.session_state.mcq_answers[question] = user_answer
            st.session_state.mcq_correct_answers[question] = answers[idx]

            if st.session_state.mcq_submitted:
                if user_answer is None:
                    st.warning(f'No answer selected')
                else:
                    if selected_index == mapping[answers[idx]]:
                        st.success(f'Correct! {answers[idx]} is the right answer', icon="✅")
                    else:
                        st.error(f'Incorrect! The correct answer is {answers[idx]}', icon="❌")

        submit_button = st.button(label='Submit Answers')

        if submit_button:
            st.session_state.mcq_submitted = True
            st.rerun()
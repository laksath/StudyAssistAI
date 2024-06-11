import streamlit as st
from helper.mcq_gpt import *

def mcq_generator():
    st.title("MCQ Generator")

    # Initialize session state variables
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ''
    if 'passage' not in st.session_state:
        st.session_state.passage = ''
    if 'no_of_questions' not in st.session_state:
        st.session_state.no_of_questions = 5
    if 'mcq_response' not in st.session_state:
        st.session_state.mcq_response = ''
    if 'input_attempted' not in st.session_state:
        st.session_state.input_attempted = False

    # Input fields
    api_key = st.text_input("Enter your API key", type='password', value=st.session_state.api_key)
    passage = st.text_area("Enter Topic or Text:", value=st.session_state.passage)
    no_of_questions = st.number_input("Enter Number of Questions:", min_value=1, value=st.session_state.no_of_questions)

    st.session_state.api_key = api_key
    st.session_state.passage = passage
    st.session_state.no_of_questions = no_of_questions

    # Generate MCQs button
    if st.button('Generate MCQs'):
        print("@@@")
        st.session_state.input_attempted = True
        if api_key and passage and no_of_questions:
            try:
                st.session_state.mcq_response = generate_mcq_response(api_key, passage, no_of_questions)
            except Exception as e:
                print("****")
                st.error(f'An error occurred: {e}')
        else:
            st.session_state.mcq_response = None

    # Show error message only if input has been attempted and data not fetched
    if st.session_state.input_attempted and not st.session_state.mcq_response:
        st.error("Please fill in all the fields correctly.")

    if st.session_state.mcq_response:
        st.subheader('Generated MCQs:')
        questions, choices, answers = parse_mcq_prompt(st.session_state.mcq_response)

        for idx, question in enumerate(questions):
            st.write(f"Q{idx + 1}: {question}")
            for choice in choices[idx]:
                st.write(choice)
            st.write(f"**Answer: {answers[idx]}**")

# Call the function to execute the page
if __name__ == "__main__":
    mcq_generator()
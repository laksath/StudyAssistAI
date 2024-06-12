import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from helper.youtube_gpt import *
from helper.mcq_gpt import parse_mcq_prompt

def youtube_video_quiz():
    st.title('YouTube Video Summarizer and Quiz Generator')
    st.write("We summarize the YouTube videos and generate quizzes for you so you don't have to.")

    # Initialize session state variables
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ''
    if 'video_url' not in st.session_state:
        st.session_state.video_url = ''
    if 'full_transcript' not in st.session_state:
        st.session_state.full_transcript = ''
    if 'summary' not in st.session_state:
        st.session_state.summary = ''
    if 'mcqs' not in st.session_state:
        st.session_state.mcqs = ''
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'correct_answers' not in st.session_state:
        st.session_state.correct_answers = {}
    if 'show_transcript' not in st.session_state:
        st.session_state.show_transcript = False
    if 'show_summary' not in st.session_state:
        st.session_state.show_summary = False
    if 'show_mcqs' not in st.session_state:
        st.session_state.show_mcqs = False
    if 'input_attempted' not in st.session_state:
        st.session_state.input_attempted = False
    if 'data_fetched' not in st.session_state:
        st.session_state.data_fetched = False

    # Input fields
    api_key = st.text_input("Enter your API key", type='password', value=st.session_state.api_key)
    video_url = st.text_input('Enter the YouTube Video URL:', value=st.session_state.video_url)

    st.session_state.api_key = api_key
    st.session_state.video_url = video_url

    def fetch_transcript(video_id):
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        full_transcript = " ".join([t['text'] for t in transcript_list])
        return full_transcript

    def summarize_transcript(api_key, full_transcript):
        return generate_yt_gpt_response(api_key, generate_summary_prompt(full_transcript), 4000)

    def generate_mcqs(api_key, full_transcript):
        return generate_yt_gpt_response(api_key, generate_yt_mcq_prompt(full_transcript), 4000)

    # Fetch video data button
    if st.button('Fetch Video Data'):
        st.session_state.input_attempted = True
        video_id = extract_video_id(video_url)
        if api_key and video_id:
            try:
                st.session_state.full_transcript = fetch_transcript(video_id)
                st.session_state.summary = ''  # Reset summary
                st.session_state.mcqs = ''  # Reset MCQs
                st.session_state.data_fetched = True
            except Exception as e:
                st.error(f'An error occurred: {e}')
        else:
            st.session_state.data_fetched = False

    # Show error message only if input has been attempted and data not fetched
    if st.session_state.input_attempted and not st.session_state.data_fetched:
        st.error("Please enter a valid YouTube video URL.")

    mapping = {
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3
    }
    
    if st.session_state.data_fetched:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button('View Transcript'):
                st.session_state.show_transcript = True
                st.session_state.show_summary = False
                st.session_state.show_mcqs = False
        with col2:
            if st.button('View Summary'):
                st.session_state.show_transcript = False
                st.session_state.show_summary = True
                st.session_state.show_mcqs = False
        with col3:
            if st.button('Generate MCQs'):
                st.session_state.show_transcript = False
                st.session_state.show_summary = False
                st.session_state.show_mcqs = True

        if st.session_state.show_transcript:
            st.subheader('Transcript:')
            st.write(st.session_state.full_transcript)

        if st.session_state.show_summary:
            if st.session_state.summary == '':
                st.session_state.summary = summarize_transcript(api_key, st.session_state.full_transcript)
            st.subheader('Summary:')
            st.write(st.session_state.summary)

        if st.session_state.show_mcqs:
            if st.session_state.mcqs == '':
                st.session_state.mcqs = generate_mcqs(api_key, st.session_state.full_transcript)
            
            st.subheader('MCQs:')
            questions, choices, answers = parse_mcq_prompt(st.session_state.mcqs)
            
            for idx, question in enumerate(questions):
                st.write(f"Q{idx + 1}: {question}")

                # Use the session state to set the initial selected value
                if question not in st.session_state.answers:
                    st.session_state.answers[question] = None

                # Determine the index of the previously selected answer, if it exists
                selected_index = None
                if st.session_state.answers[question]:
                    try:
                        selected_index = choices[idx].index(st.session_state.answers[question])
                    except ValueError:
                        selected_index = None

                user_answer = st.radio(
                    "Select your answer:", choices[idx], 
                    key=f"{question}_options",
                    index=selected_index
                )

                # Update session state with the selected answer immediately
                st.session_state.answers[question] = user_answer
                st.session_state.correct_answers[question] = answers[idx]

                if st.session_state.submitted:
                    if user_answer is None:
                        st.warning(f'No answer selected')
                    else:
                        if selected_index == mapping[answers[idx]]:
                            st.success(f'Correct! {answers[idx]} is the right answer', icon="✅")
                        else:
                            st.error(f'Incorrect! The correct answer is {answers[idx]}', icon="❌")

            submit_button = st.button(label='Submit Answers')

            if submit_button:
                st.session_state.submitted = True
                st.rerun()
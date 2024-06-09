import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from helper.youtube_gpt import *
import re
from urllib.parse import urlparse, parse_qs

def youtube_video_quiz():
    st.title('YouTube Video Summarizer and Quiz Generator')
    st.write("We summarize the YouTube videos and generate quizzes for you so you don't have to.")

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

    api_key = st.text_input("Enter your API key", type='password', value=st.session_state.api_key)
    video_url = st.text_input('Enter the YouTube Video URL:', value=st.session_state.video_url)

    st.session_state.api_key = api_key
    st.session_state.video_url = video_url

    def extract_video_id(url):
        """
        Extracts the YouTube video ID from the given URL.
        """
        video_id = None
        match = re.match(r'(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+', url)
        if match:
            if 'youtube.com' in url:
                query = urlparse(url).query
                video_id = parse_qs(query).get('v')
                if video_id:
                    video_id = video_id[0]
            elif 'youtu.be' in url:
                video_id = url.split('/')[-1]
        return video_id

    @st.cache_data
    def fetch_transcript(video_id):
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        full_transcript = " ".join([t['text'] for t in transcript_list])
        return full_transcript

    @st.cache_data
    def summarize_transcript(api_key, full_transcript):
        return generate_yt_gpt_response(api_key, generate_summary_prompt(full_transcript), 4000)

    @st.cache_data
    def generate_mcqs(api_key, full_transcript):
        return generate_yt_gpt_response(api_key, generate_mcq_prompt(full_transcript), 4000)

    video_id = extract_video_id(video_url)
    if api_key and video_id:
        try:
            if st.session_state.full_transcript == '':
                st.session_state.full_transcript = fetch_transcript(video_id)

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
                questions = st.session_state.mcqs.split('\n\n')  # Assuming each question is separated by a blank line

                for q in questions:
                    try:
                        parts = q.strip().split('\n')
                        question = parts[0]
                        options = parts[1:5]
                        answer = parts[5]
                        correct_answer = answer.split(': ')[1].strip()

                        st.write(question)

                        # Use the session state to set the initial selected value
                        if question not in st.session_state.answers:
                            st.session_state.answers[question] = None

                        user_answer = st.radio(
                            "Select your answer:", options, 
                            key=f"{question}_options",
                            index=options.index(st.session_state.answers[question]) if st.session_state.answers[question] else None
                        )

                        # Update session state with the selected answer immediately
                        st.session_state.answers[question] = user_answer
                        st.session_state.correct_answers[question] = correct_answer

                        if st.session_state.submitted:
                            if user_answer is None:
                                st.warning(f'No answer selected')
                            else:
                                if user_answer.strip() == correct_answer:
                                    st.success(f'Correct! {correct_answer} is the right answer', icon="✅")
                                else:
                                    st.error(f'Incorrect! The correct answer is {correct_answer}', icon="❌")
                    except IndexError:
                        st.error(f"An error occurred while processing the question: {q}")

                submit_button = st.button(label='Submit Answers')

                if submit_button:
                    st.session_state.submitted = True
                    st.experimental_rerun()

        except Exception as e:
            st.error(f'An error occurred: {e}')
    else:
        st.error("Please enter a valid YouTube video URL.")
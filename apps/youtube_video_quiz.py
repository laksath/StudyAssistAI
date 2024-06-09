import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from gpts.youtube_gpt import *
import re
from urllib.parse import urlparse, parse_qs

def youtube_video_quiz():
    
    st.title('YouTube Video Summarizer and Quiz Generator')
    st.write("We summarize the YouTube videos and generate quizzes for you so you don't have to.")

    api_key = st.text_input("Enter your API key", type='password')
    video_url = st.text_input('Enter the YouTube Video URL:', '')

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
            full_transcript = fetch_transcript(video_id)

            col1, col2, col3 = st.columns(3)
            with col1:
                show_transcript = st.button('View Transcript')
            with col2:
                show_summary = st.button('View Summary')
            with col3:
                show_mcqs = st.button('Generate MCQs')

            if show_transcript:
                st.subheader('Transcript:')
                st.write(full_transcript)

            if show_summary:
                summary = summarize_transcript(api_key, full_transcript)
                st.subheader('Summary:')
                st.write(summary)

            if show_mcqs or 'mcqs' in st.session_state:
                if show_mcqs:
                    st.session_state.mcqs = generate_mcqs(api_key, full_transcript)
                
                st.subheader('MCQs:')
                questions = st.session_state.mcqs.split('\n\n')  # Assuming each question is separated by a blank line

                if 'answers' not in st.session_state:
                    st.session_state.answers = {}
                    st.session_state.correct_answers = {}

                with st.form(key='mcq_form'):
                    for q in questions:
                        try:
                            parts = q.strip().split('\n')
                            question = parts[0]
                            options = parts[1:5]
                            answer = parts[5]
                            correct_answer = answer.split(': ')[1].strip()

                            st.write(question)
                            user_answer = st.radio("Select your answer:", options, key=question, index=None)
                            st.session_state.correct_answers[question] = correct_answer
                            st.session_state.answers[question] = user_answer

                            if 'submitted' in st.session_state and st.session_state.submitted:
                                if user_answer is None:
                                    st.warning(f'No answer selected')
                                else:
                                    if user_answer.strip() == correct_answer:
                                        st.success(f'Correct! {correct_answer} is the right answer', icon="✅")
                                    else:
                                        st.error(f'Incorrect! The correct answer is {correct_answer}', icon="❌")
                        except IndexError:
                            st.error(f"An error occurred while processing the question: {q}")

                    submit_button = st.form_submit_button(label='Submit Answers')

                    if submit_button:
                        st.session_state.submitted = True
                        st.experimental_rerun()

        except Exception as e:
            st.error(f'An error occurred: {e}')
    else:
        st.error("Please enter a valid YouTube video URL.")
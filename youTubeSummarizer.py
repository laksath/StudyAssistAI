import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import requests
import json

st.title('YouTube Video Summarizer and Quiz Generator')
st.write("We summarize the YouTube videos and generate quizzes for you so you don't have to.")

api_key = st.text_input("Enter your API key", type='password')
video_id = st.text_input('Enter the YouTube Video ID:', '')

def generate_gpt_response(api_key, instruction, max_tokens):
    endpoint = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        'model': 'gpt-4-0613',  # or the model of your choice
        'messages': [{'role': 'user', 'content': instruction}],
        'max_tokens': max_tokens  # change this to whatever you want
    }

    response = requests.post(endpoint, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        json_response = response.json()
        summary = json_response['choices'][0]['message']['content'].strip()
        return summary
    else:
        raise Exception(f"Error in API request: {response.status_code}, {response.text}")

@st.cache_data
def fetch_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    full_transcript = " ".join([t['text'] for t in transcript_list])
    return full_transcript

@st.cache_data
def summarize_transcript(api_key, full_transcript):
    return generate_gpt_response(
        api_key,
        f'Summarize the following text using bullet points: {full_transcript}',
        4000
    )

@st.cache_data
def generate_mcqs(api_key, full_transcript):
    return generate_gpt_response(
        api_key,
        f'Generate 5 multiple-choice questions based on the following text: {full_transcript}. Format the questions and options as follows: Q1. Question? a) Option 1 b) Option 2 c) Option 3 d) Option 4. Provide the correct answer at the end of each question with "Answer: option".',
        4000
    )

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

        if show_mcqs:
            mcqs = generate_mcqs(api_key, full_transcript)
            st.subheader('MCQs:')
            questions = mcqs.split('\n\n')  # Assuming each question is separated by a blank line
            for q in questions:
                question, *options, answer = q.split('\n')
                correct_answer = answer.split(': ')[1].strip()
                
                st.write(question)
                user_answer = st.radio(question, options)
                
                if st.button(f'Submit Answer for {question}'):
                    if user_answer == correct_answer:
                        st.success(f'Correct! {correct_answer} is the right answer.', icon="✅")
                    else:
                        st.error(f'Incorrect! The correct answer is {correct_answer}.', icon="❌")
    except Exception as e:
        st.error(f'An error occurred: {e}')
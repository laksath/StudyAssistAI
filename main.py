import streamlit as st
from apps import home, youtube_video_quiz, worksheet_generator, page3

def main():
    st.sidebar.title("Navigation")
    pages = {
        "Home": home.home_page,
        "YouTube Video Summarizer and Quiz Generator": youtube_video_quiz.youtube_video_quiz,
        "Worksheet Generator": worksheet_generator.worksheet_generator,
        "Multiple Choice Assessments": page3.page3,
    }
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    pages[selection]()

if __name__ == "__main__":
    main()
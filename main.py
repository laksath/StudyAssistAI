import streamlit as st
from apps import home, youtube_video_quiz, page2, page3

def main():
    st.sidebar.title("Navigation")
    pages = {
        "Home": home.home_page,
        "YouTube Video Summarizer and Quiz Generator": youtube_video_quiz.youtube_video_quiz,
        "Page 2": page2.page2,
        "Page 3": page3.page3,
    }
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    pages[selection]()

if __name__ == "__main__":
    main()
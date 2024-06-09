import streamlit as st

def home_page():
    st.title("Welcome to StudyAssist AI")
    st.header("Your AI-Powered Study Companion")

    # Introduction and Overview
    st.write("""
    StudyAssist AI is designed to help you learn and study more effectively using the power of artificial intelligence. 
    Whether you're preparing for exams, trying to understand new concepts, or seeking to improve your knowledge, 
    StudyAssist AI offers personalized assistance to meet your learning needs.
    """)

    # Highlight Features
    st.subheader("Key Features:")

    # Worksheet Generator
    st.markdown("""
    ### Worksheet Generator
    Generate a worksheet based on any topic or text. 
    - Input your topic or text, and the AI will create a customized worksheet to help reinforce your learning.
    - Includes a variety of questions and exercises tailored to the material.
    """)

    # Multiple Choice Assessments
    st.markdown("""
    ### Multiple Choice Assessments
    Create a multiple choice assessment based on any topic, standard, or criteria.
    - Select the topic and criteria, and the AI will generate a comprehensive multiple choice test.
    - Perfect for self-assessment and exam preparation.
    """)

    # YouTube Video Questions
    st.markdown("""
    ### YouTube Video Questions
    Generate guiding questions aligned to a YouTube video.
    - Provide the URL of a YouTube video, and the AI will create questions that guide your understanding of the video content.
    - Ideal for integrating multimedia resources into your study routine.
    """)

    # Text Dependent Questions
    st.markdown("""
    ### Text Dependent Questions
    Generate text-based questions based on any topic, standard, or material.
    - Input your text, topic, or material, and the AI will generate insightful questions that promote deeper understanding.
    - Useful for critical reading and analysis practice.
    """)

    # Call to Action
    st.subheader("Get Started")
    st.write("Navigate through the sidebar to explore various features and start your learning journey with StudyAssist AI!")

    # Footer or additional information
    st.write("""
    ---
    Created by [Your Name or Company]
    """)
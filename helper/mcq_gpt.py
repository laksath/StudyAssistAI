from openai import OpenAI
import os
import re

def generate_mcq_prompt(passage, number_of_questions):
    prompt = f"""I need multiple-choice questions (MCQs) based on the following passage or essay: '{passage}'. Each question should have 4 options labeled A, B, C, and D. Provide the correct answer after each question in a separate line starting with 'Answer: '. Ensure there is a clear separator between each question and its corresponding answer. Follow the format exactly as shown below:

Q1: Question text here
A) Option 1
B) Option 2
C) Option 3
D) Option 4
Answer: B

Q2: Question text here
A) Option 1
B) Option 2
C) Option 3
D) Option 4
Answer: C

Q3: Question text here
A) Option 1
B) Option 2
C) Option 3
D) Option 4
Answer: A

Repeat this format for {number_of_questions} questions."""
    return prompt
  
def generate_worksheet_response(api_key, topic_or_text, no_of_questions):
    prompt = generate_mcq_prompt(topic_or_text, no_of_questions)
    
    client = OpenAI(
        api_key=os.getenv(api_key)
    )
    
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content

def parse_mcq_prompt(prompt):
    # Define regular expressions for questions, choices, and answers
    question_re = re.compile(r'Q\d+: (.*?)\n')
    choice_re = re.compile(r'[A-D]\) (.*?)\n')
    answer_re = re.compile(r'Answer: ([A-D])')

    questions = question_re.findall(prompt)
    choices = []
    answers = answer_re.findall(prompt)

    # Extract choices for each question
    all_choices = choice_re.findall(prompt)
    for i in range(0, len(all_choices), 4):
        choices.append(all_choices[i:i+4])

    return questions, choices, answers

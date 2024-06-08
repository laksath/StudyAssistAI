from openai import OpenAI
import os

def gpt4o_text_generation(prompt):
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY')
    )

    response = client.images.generate(
        model="gpt-4o",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )

    image_url = response.data[0].url
    return image_url

def generate_prompt(grade_level, topic_or_text):
    prompt = f"""
    You are an experienced educational content creator. I need you to generate a worksheet for students based on the following information:

    1. Grade Level: {grade_level}
    2. Topic or Text: {topic_or_text}

    Worksheet Requirements:

    1. Topic Description: Provide a very brief description of the topic suitable for the specified grade level.
    2. Fill in the Blanks Questions: Create 5 fill-in-the-blank questions related to the topic.
    3. Word Bank: Provide a word bank that includes the correct answers for the fill-in-the-blank questions and additional relevant terms.
    4. Multiple Choice Questions: Develop 5 multiple-choice questions, each with four answer options, related to the topic.
    5. Open-Ended Questions: Create 3 open-ended questions that encourage critical thinking and deeper understanding of the topic.
    6. Answer Key: Provide the correct answers for the fill-in-the-blank questions, multiple-choice questions, and open-ended questions at the end of the worksheet.
    """
    
    return prompt

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def generate_response(prompt):
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    )

    return completion.choices[0].message['content']
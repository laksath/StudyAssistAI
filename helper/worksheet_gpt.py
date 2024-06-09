from openai import OpenAI
import os

def generate_prompt(grade_level, topic_or_text):
    prompt = f"""
    You are an experienced educational content creator. I need you to generate a worksheet for students based on the following information:

    1. Grade Level: {grade_level}
    2. Topic or Text: {topic_or_text}

    Please follow this exact structure and format for the response to ensure uniformity:

    ---

    ### Topic Description
    Provide a very brief description of the topic suitable for the specified grade level.

    ### Fill in the Blanks Questions
    1. _______
    2. _______
    3. _______
    4. _______
    5. _______

    ### Word Bank
    - 
    - 
    - 
    - 
    - 
    - 
    - 
    - 
    - 

    ### Multiple Choice Questions
    1. Which event is commonly recognized as the beginning of World War Two?
        a) 
        b) 
        c) 
        d) 

    2. What was the main objective of the D-Day Normandy landings?
        a) 
        b) 
        c) 
        d) 

    3. Which country was NOT part of the Axis Powers?
        a) 
        b) 
        c) 
        d) 

    4. The Battle of Britain was primarily fought between which two nations?
        a) 
        b) 
        c) 
        d) 

    5. What significant event led the United States to enter World War Two?
        a) 
        b) 
        c) 
        d) 

    ### Open-Ended Questions
    1. Discuss the significance of the Normandy landings for the Allied victory in World War Two. How did this event shape the outcome of the war?
    2. Analyze the impact of the Battle of Britain on the Luftwaffe's strategies and the overall war outcome. Why was this battle a turning point?
    3. Explain how the entry of the United States into World War Two altered the dynamics of the conflict. What were some consequences for the Allied and Axis powers?

    ### Answer Key
    #### Fill in the Blanks Questions
    1. 
    2. 
    3. 
    4. 
    5. 

    #### Multiple Choice Questions
    1. 
    2. 
    3. 
    4. 
    5. 

    #### Open-Ended Questions
    1. 
    2. 
    3. 

    ---
    """
    return prompt

def generate_worksheet_response(api_key, grade_level, topic_or_text):
    prompt = generate_prompt(grade_level, topic_or_text)
    
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
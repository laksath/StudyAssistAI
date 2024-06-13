from helper.gpt import completion

def generate_comprehension_prompt(text, num_questions, grade_level):
    prompt = f"""
    Create {num_questions} comprehension questions and an answer key for the following text at a {grade_level} grade level:
    
    Text:
    {text}
    
    The format should be:
    
    Comprehension Questions on [Topic]:
    1. [Question 1]
    2. [Question 2]
    3. [Question 3]
    ...
    
    Answer Key:
    1. [Answer 1]
    2. [Answer 2]
    3. [Answer 3]
    ...
    
    Example:
    
    Comprehension Questions on World War II:
    1. What were the two main alliances involved in World War II, and how did they impact the conflict?
    2. How did aircraft play a significant role in World War II, and what were some of the consequences of their use?
    3. What were some of the contributing factors to the outbreak of World War II as mentioned in the text?
    
    Answer Key:
    1. The two main alliances were the Allies and the Axis powers. They involved nearly all of the world's countries and influenced the war through economic, industrial, and scientific capabilities.
    2. Aircraft played a major role in enabling strategic bombing and the delivery of nuclear weapons, leading to high fatalities and devastation.
    3. Some contributing factors to the outbreak of World War II included the rise of fascism in Europe, the Spanish Civil War, the Second Sino-Japanese War, Soviet-Japanese border conflicts, and tensions from the aftermath of World War I.
    """
    return prompt

def generate_comprehension_response(api_key, grade_level, num_questions, text):
    prompt = generate_comprehension_prompt(text, num_questions, grade_level)
    return completion(api_key, 'gpt-4o', prompt)
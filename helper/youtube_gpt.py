import requests
import json

def generate_summary_prompt(full_transcript):
    return f"Summarize the following text using bullet points: {full_transcript}"

def generate_mcq_prompt(full_transcript):
    return f'Generate 5 multiple-choice questions based on the following text: {full_transcript}. Format the questions and options as follows: Q1. Question? a) Option 1 b) Option 2 c) Option 3 d) Option 4. Provide the correct answer at the end of each question with "Answer: option".'

def generate_yt_gpt_response(api_key, instruction, max_tokens):
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

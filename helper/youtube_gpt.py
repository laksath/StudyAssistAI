import requests
import json
import re
from urllib.parse import urlparse, parse_qs
from helper.mcq_gpt import generate_mcq_prompt

def generate_summary_prompt(full_transcript):
    return f"Summarize the following text using bullet points: {full_transcript}"

def generate_yt_mcq_prompt(full_transcript):
    return generate_mcq_prompt(full_transcript, 5)

def generate_yt_gpt_response(api_key, instruction, max_tokens):
    endpoint = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        'model': 'gpt-4o',  # or the model of your choice
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

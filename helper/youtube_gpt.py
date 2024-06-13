import re
from urllib.parse import urlparse, parse_qs
from helper.mcq_gpt import generate_mcq_prompt
from helper.gpt import completion

def generate_summary_prompt(full_transcript):
    return f"Summarize the following text using bullet points: {full_transcript}"

def generate_yt_mcq_prompt(full_transcript):
    return generate_mcq_prompt(full_transcript, 5)

def generate_yt_gpt_response(api_key, prompt, max_tokens):
    return completion(api_key, 'gpt-4o', prompt, max_tokens)
    
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

from openai import OpenAI
import tiktoken

def completion(api_key, model, prompt, max_tokens=None):
    client = OpenAI(api_key=api_key)
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    
    if max_tokens is None:
        completion = client.chat.completions.create(
            model=model,
            messages=messages
        )
    else:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens
        )

    return completion.choices[0].message.content.strip()

def num_tokens_from_string(string: str, encoding_name: str): # 'o200k_base'
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens
from openai import OpenAI
import tiktoken
import time

def completion(api_key, model, prompt, max_tokens=None):
    # start_time = time.time()
    
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

    # end_time = time.time()
    # print(f"GPT execution_time: {end_time - start_time} seconds.")
    # print(f"Tokens Consumed: {completion.to_dict()['usage']['total_tokens']}")
    return completion.choices[0].message.content.strip()

def num_tokens_from_string(string, encoding_name = 'o200k_base'):
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens
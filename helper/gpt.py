from openai import OpenAI

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
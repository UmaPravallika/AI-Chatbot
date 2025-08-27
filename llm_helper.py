from openai import OpenAI
from config import Config

# System Prompt
system_prompt=Config.SYSTEM_PROMPT

def chat(user_prompt,model,temperature=0.7,max_tokens=200):
    client=OpenAI()
    completion=client.chat.completions.create(
        model=model,
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True
    )
    return completion


def stream_parser(stream):
    for chunk in stream : 
        if chunk.choices[0].delta.content!=None:
            yield chunk.choices[0].delta.content

        
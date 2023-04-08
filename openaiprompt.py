# code to use openai gpt

import openai
import os

# set the api key
openai.api_key = "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"

# prompt
prompt = """What are animals ?"""

# response
response = openai.Completion.create(
    engine="davinci",
    prompt=prompt,
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=["\n", "This concludes this test of the emergency broadcast system."]
)

# print the response
print(response.choices[0].text)
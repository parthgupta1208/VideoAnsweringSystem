import openai
import requests

openai.api_key = "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"

response = requests.post(
    "https://api.openai.com/v1/engines/davinci/completions",
    headers={"Authorization": f"Bearer {openai.api_key}"},
    json={
        "prompt": "What are animals",
        "temperature": 0.5,
        "max_tokens": 50,
    },
)


print(response.json()['choices'][0]['text'])

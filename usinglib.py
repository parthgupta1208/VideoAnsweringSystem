import openai

openai.api_key = "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"

prompt = input()

response = openai.Completion.create(
    engine="gpt-3.5-turbo",
    prompt=prompt,
    max_tokens=300,
    temperature=0.7,
    # top_p=0.5,
    # frequency_penalty=1.0,
    # presence_penalty=1.0,

)

print(response)

import openai
def get_response(prompt):
    openai.api_key = "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"
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages = [{"role": "system", "content" : "You are FridayAI, a large language model trained by Parth Gupta. Answer as concisely as possible.\nKnowledge cutoff: 2021-09-01\nCurrent date: 2023-04-10"},
    {"role": "user", "content" : "How are you?"},
    {"role": "assistant", "content" : "I am doing well"},
    {"role": "user", "content" : prompt}]
    )
    return completion['choices'][0]['message']['content']
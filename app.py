from openai import OpenAI

api_key = "sk-1234567890abcdefghijklmnopqrstuvwxYZABCDEF"

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Example: send a prompt to the GPT model
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a haiku about debugging Python code."},
    ]
)

# Print the model's reply
print(response.choices[0].message.content)

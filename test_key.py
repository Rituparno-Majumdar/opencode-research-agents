import os
from openai import OpenAI

# Test with the new key
client = OpenAI(
    api_key="sk-WQ4BrEuB10ELuB2WVe1F1hVOr1NSJTQjSpBV4pHIRnZa5WPxfRv5WLCQQdm1aPK6",
    base_url="https://api.opencode.ai/v1"
)

response = client.chat.completions.create(
    model="minimax-m2.5-free",
    messages=[{"role": "user", "content": "Say 'test OK' in 2 words"}],
    max_tokens=20
)
print(response.choices[0].message.content)
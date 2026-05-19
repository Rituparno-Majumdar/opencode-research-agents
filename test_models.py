import os
from openai import OpenAI

client = OpenAI(
    api_key="sk-WQ4BrEuB10ELuB2WVe1F1hVOr1NSJTQjSpBV4pHIRnZa5WPxfRv5WLCQQdm1aPK6",
    base_url="https://api.opencode.ai/v1"
)

# Try different model names
models_to_try = [
    "minimax-m2.5-free",
    "minimax-m2.1-free", 
    "minimax-m1-free",
    "minimax/free",
    "default"
]

for model in models_to_try:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say 'OK' in 2 words"}],
            max_tokens=20
        )
        print(f"Model {model} worked: {response}")
    except Exception as e:
        print(f"Model {model} failed: {e}")
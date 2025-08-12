import requests
from config import DEEPINFRA_API_KEY

def get_deepinfra_response(prompt):
    headers = {
        "Authorization": f"Bearer {DEEPINFRA_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        res = requests.post("https://api.deepinfra.com/v1/openai/chat/completions", headers=headers, json=data)
        res.raise_for_status()
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        print("❌ DeepInfra Error:", e)
        return "Sorry, I couldn't reach the AI service."

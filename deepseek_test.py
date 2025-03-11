import requests
import json

# API key and setup
API_KEY = "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"
URL = "https://openrouter.ai/api/v1/chat/completions"

# Headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:8501",  
    "X-Title": "Maternity Chatbot"            
}

# Payload
payload = {
    "model": "deepseek/deepseek-r1:free",
    "messages": [
        {
            "role": "user",
            "content": "What is the meaning of life?"
        }
    ]
}

# Make the request
response = requests.post(
    url=URL,
    headers=headers,
    data=json.dumps(payload)
)

# Check the response
if response.status_code == 200:
    result = response.json()
    print("Response from DeepSeek:")
    print(result["choices"][0]["message"]["content"])
else:
    print(f"Error: {response.status_code}")
    print(response.text)
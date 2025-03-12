import requests
import os

API_URL = "https://api.together.xyz/v1/chat/completions"
API_KEY = os.getenv("API_KEY")  # Get API Key from environment
 # Store securely

def summarize_document(text):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "messages": [
            {"role": "system", "content": "You are an AI that provides concise and accurate summaries of documents."},
            {"role": "user", "content": f"Summarize this document: {text}"}
        ],
        "temperature": 0.5
    }

    response = requests.post(API_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

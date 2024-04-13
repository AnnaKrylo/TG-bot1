import requests
import os
from dotenv import load_dotenv

load_dotenv()
model_uri = os.getenv('MODEL')
iam_token = os.getenv('TOKEN2')
gpt_url = os.getenv('GPT_URL')


def get_advice(text):
    print("sending request...")
    query = {
        "modelUri": model_uri,
        "completionOptions": {
            "stream": False,
            "temperature": 0.3,
            "maxTokens": 2000
        },
        "messages": [
            {
                "role": "user",
                "text": "улучши текст для устного выступления: " + text
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key " + iam_token
    }
    response = requests.post(gpt_url, json=query,
                             headers=headers)
    answer = response.json()

    return answer['result']['alternatives'][0]['message']['text']

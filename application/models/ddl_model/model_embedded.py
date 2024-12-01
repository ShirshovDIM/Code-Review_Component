import requests
import json
import asyncio


def get_evrazgpt_response(user_prompt: str, 
                          system_context = "answer in english", 
                          max_tokens=1024, 
                          temperature=.3, 
                          return_json=False) -> str:
    url = "http://84.201.152.196:8020/v1/completions"
    headers = {
        "Authorization": "Df5OqALNrsio9ynQYqZgOoO5erPJrL2n",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-nemo-instruct-2407",
        "messages": [
            {
                "role": "system",
                "content": system_context 
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }



    response = requests.post(url, headers=headers, data=json.dumps(payload))
    content = response.json()["choices"][0]["message"]["content"]
    print(content)

    print(f"Status Code: {response.status_code}")

    if return_json: 
        with open('responce.json', 'w') as file :
            json.dump(response.json(), file) 


    return content

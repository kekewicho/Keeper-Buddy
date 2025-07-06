import requests
import os

def prompt(chat):
    
    llm_host = os.getenv("LLM_HOST", "127.0.0.1")
    llm_port = os.getenv("LLM_PORT", "8001")
    
    response = requests.post(
        f"http://{llm_host}:{llm_port}/prompt",
        headers={"Content-Type": "application/json"},
        json=chat
    )

    return response.json()



def build_user_message(message):

    return {
        "role": "user",
        "parts": [
            {
                "text": message
            }
        ]
    }

def build_function_response(name, response):


    return {
        "parts": [
            {
                "function_response": {
                    "name": name,
                    "response": response
                }
            }
        ],
        "role": "user"
    }
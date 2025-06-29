import requests

def prompt(chat):
    
    response = requests.post(
        "http://127.0.0.1:8001/prompt",
        headers={"Content-Type": "application/json"},
        json=chat
    )

    return response.json()



def build_user_message(message):

    return {
        "role": "user",
        "parts": [
            {
                "content": {
                    "text": message
                },
                "part_type": "message"
            }
        ]
    }

def build_function_response(name, response):

    return {
        "parts": [
            {
                "content": {
                    "name": name,
                    "response": response
                },
                "part_type": "function_response"
            }
        ],
        "role": "user"
    }
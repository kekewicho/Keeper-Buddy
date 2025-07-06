import requests
import os
import json

def prompt(chat):
    
    llm_url = os.getenv("LLM_URL", "http://127.0.0.1:8001")
    
    response = requests.post(
        f"{llm_url}/prompt",
        headers={"Content-Type": "application/json"},
        json=chat
    )

    return response.json()



def build_user_message(message: str, personalization_JID: str = None):

    personalization_prompt = get_personalization_for_JID(personalization_JID) or ""

    return {
        "role": "user",
        "parts": [
            {
                "text": personalization_prompt + message
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



def get_personalization_for_JID(JID) -> list:
    """
    This function should retrieve the personalization data for a given JID.
    For now, it returns None as a placeholder.
    """

    with open(os.getenv("LLM_CONFIG_PATH","LLM.config.json"), "r") as file:
        
        config_params = json.loads(file.read())

        personalization = config_params.get("personalization")

        if not personalization:
            return None
        

        for config_jid, data in personalization.items():

            
            if config_jid in JID:
                return '. '.join(data) + ". "
        return None
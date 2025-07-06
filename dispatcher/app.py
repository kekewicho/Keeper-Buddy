from flask import Flask, request, jsonify
import requests
from utils.prompt import build_user_message, prompt, build_function_response
from dotenv import load_dotenv
import os
from model.message_model import Message
from model.chat_model import Chat

load_dotenv()


MAX_ITERATIONS = 5


app = Flask(__name__)


@app.route('/', methods=['POST'])
def webhook():
    data = request.json

    message = data["data"]["message"]["conversation"]
    jid = data["data"]["key"]["remoteJid"]
    json_message = build_user_message(message, jid)
    
    actual_chat = Chat([Message(json_message)])

    actual_iteration = 0

    while actual_iteration < MAX_ITERATIONS:

        last_message = actual_chat[-1]

        if last_message.role == "model" and last_message.is_text:
            break


        actual_iteration += 1

        response = Message(prompt(actual_chat.to_json())[-1])


        actual_chat.append(response)

        if response.is_function_call:

            function_call_data = response.function_call_data
        
            name = function_call_data["name"]
            keeper_service_url = os.getenv("KEEPER_SERVICE_URL", "http://127.0.0.1:8003")
            func_response = requests.post(
                url=f"{keeper_service_url}/{name}",
                json=function_call_data['args'],
                headers={"Content-Type": "application/json"}
            ).json()

            response = Message(build_function_response(name, func_response))

            actual_chat.append(response)


    response_to_user = actual_chat[-1].text_content
    
    try:
        send_message(response_to_user, data["data"]["key"]["remoteJid"])

        return jsonify({"status": "success", "message": response_to_user}), 200
    
    except Exception as e:

        return jsonify({"status": "error", "message": actual_chat.to_json()}), 500


def send_message(message, to):

    evolution_url = os.getenv("EVOLUTION_API_URL", "http://127.0.0.1:8080")
    evolution_instance = os.getenv("EVOLUTION_INSTANCE", "default")

    requests.request(
        "POST",
        url = f"{evolution_url}/message/sendText/{evolution_instance}",
        json = {
            "number": "+" + to,
            "text": message,
            "delay": 750
        },
        headers = {
            "Content-Type": "application/json",
            "apiKey": os.getenv("AUTHENTICATION_API_KEY")
        }
    )




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002, debug=True)
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

    isFromMe = data["data"]["key"]["fromMe"]

    if not isFromMe: #(isFromMe or "4444929147" in str(data["data"]["key"]["remoteJid"])):

        return jsonify({"status": "success"}), 200

    message = data["data"]["message"]["conversation"]
    json_message = build_user_message(message)
    
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
            keeper_host = os.getenv("KEEPER_SERVICE_HOST", "127.0.0.1")
            keeper_port = os.getenv("KEEPER_SERVICE_PORT", "8003")
            func_response = requests.post(
                url=f"http://{keeper_host}:{keeper_port}/{name}",
                json=function_call_data['args'],
                headers={"Content-Type": "application/json"}
            ).json()

            response = Message(build_function_response(name, func_response))

            actual_chat.append(response)


    response_to_user = actual_chat[-1].text_content

    try:
        send_message(response_to_user, data["data"]["key"]["remoteJid"])
    

        return jsonify({"status": "success", "message": "Mensaje recibido"}), 200
    
    except Exception as e:

        return jsonify({"status": "error", "message": actual_chat.to_json()}), 500


def send_message(message, to):

    evolution_host = os.getenv("EVOLUTION_API_HOST", "127.0.0.1")
    evolution_port = os.getenv("EVOLUTION_API_PORT", "8080")

    requests.request(
        "POST",
        url = f"http://{evolution_host}:{evolution_port}/message/sendText/Test",
        json = {
            "number": "+" + to,
            "text": message,
            "delay": 750
        },
        headers = {
            "Content-Type": "application/json",
            "apiKey": "123456.+az1"
        }
    )




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002, debug=True)
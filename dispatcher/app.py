from flask import Flask, request, jsonify
import requests
from utils.prompt import build_user_message, prompt
from controllers import FUNCTION_CALLS

MAX_ITERATIONS = 5


app = Flask(__name__)


@app.route('/', methods=['POST'])
def webhook():
    data = request.json

    isFromMe = data["data"]["key"]["fromMe"]

    if not (isFromMe or "4444929147" in str(data["data"]["key"]["remoteJid"])):

        return jsonify({"status": "success"}), 200

    message = data["data"]["message"]["conversation"]

    
    actual_chat = [build_user_message(message)]
    actual_iteration = 0

    while actual_iteration < MAX_ITERATIONS:

        role = actual_chat[-1]["role"]
        _part_type = actual_chat[-1]["parts"][-1]["part_type"]

        if role == "model" and _part_type == "message":
            break


        actual_iteration += 1

        response = prompt(actual_chat)

        actual_chat = response

        part_type = response[-1]["parts"][-1]["part_type"]
        content = response[-1]["parts"][-1]["content"]

        if part_type == "function_call":

            func_response = FUNCTION_CALLS[content["name"]](**content["args"])

            actual_chat.append(func_response)

        print(actual_chat)


    response_to_user = actual_chat[-1].get("parts")[-1].get("content").get("text")

    send_message(response_to_user, data["data"]["key"]["remoteJid"])
    

    return jsonify({"status": "success", "message": "Mensaje recibido"}), 200


def send_message(message, to):


    requests.request(
        "POST",
        url = "http://127.0.0.1:8080/message/sendText/Test",
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
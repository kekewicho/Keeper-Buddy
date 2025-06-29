from flask import Flask, request
from LLM import prompt
from adapters import json_to_part, part_to_json



app = Flask(__name__)

@app.post("/prompt")
def understand_message():

    try:
        chat = request.get_json()

        content = json_to_part(chat)

        response = prompt(content)

        parsed_response = part_to_json(response)

        return parsed_response, 200
    
    except Exception as e:
        print(e)
        return str(e), 500




if __name__ == '__main__':
    app.run(debug=True, port=8001, host='0.0.0.0')

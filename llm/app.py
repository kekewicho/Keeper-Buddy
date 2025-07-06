from flask import Flask, request
from LLM import prompt



app = Flask(__name__)

@app.post("/prompt")
def understand_message():

    try:
        chat = request.get_json()

        response = prompt(chat)

        return response, 200
    
    except Exception as e:
        print(e)
        return str(e), 500




if __name__ == '__main__':
    app.run(debug=True, port=8001)

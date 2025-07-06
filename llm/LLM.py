import google.generativeai as genai 
from google.generativeai import types 
import dotenv
import os
import json

dotenv.load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))

tasks_tools_definition = json.loads(open("tools.json", "r").read())
tools = [types.Tool(function_declarations=tasks_tools_definition)]

MODEL_NAME = "gemini-2.5-flash"


def prompt(contents: list) -> list:
    try:
        model = genai.GenerativeModel(
            MODEL_NAME
        )
        
        response = model.generate_content(
            contents=contents,
            tools=tools,
        )

        return [
            *contents,
            response.to_dict()['candidates'][0]['content']
        ]
    
    except Exception as e:

        return [
            *contents,
            {
                "role": "model",
                "parts": [
                    {
                        "text": f"Ocurrio un error al procesar la solicitud: {str(e)}"
                    }
                ]
            }
        ]
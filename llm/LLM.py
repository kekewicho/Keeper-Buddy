from google import genai
from google.genai import types
import dotenv
import os
import json

dotenv.load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_AI_API_KEY"))

tasks_tools_definition = json.loads(open("tools.json", "r").read())

tools = types.Tool(function_declarations=tasks_tools_definition)
config = types.GenerateContentConfig(tools=[tools])

MODEL = "gemini-2.5-flash"


def prompt(contents:list[types.Content]) -> list[types.Content]:

    response = client.models.generate_content(
        model=MODEL,
        contents=contents,
        config=config
    )
    

    return [
        *contents,
        response.candidates[0].content
    ]

    
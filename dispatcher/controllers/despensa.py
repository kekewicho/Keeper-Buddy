import datetime as dt
import json
from utils.dates_helpers import next_paday_key
from utils.prompt import build_function_response


def add_to_shopping_list(article: str, payday: str = None):

    despensa_key = payday or next_paday_key()

    file_content = open("despensa.json", "r").read()

    actual = json.loads(file_content)

    if not actual.get(despensa_key):
        actual[despensa_key] = []

    actual[despensa_key].append({
        "article": article
    })

    with open("despensa.json", "w") as file:

        file.write(json.dumps(actual))
        file.close()

    return build_function_response(add_to_shopping_list.__name__, {"status": "success", "article": article, "payday": payday})



def show_me_the_shopping_list(payday: str = None):

    despensa_key = payday or next_paday_key()

    file_content = open("despensa.json", "r").read()

    actual = json.loads(file_content)

    key_result = actual.get(despensa_key)

    if key_result:

        return build_function_response(show_me_the_shopping_list.__name__, {"status": "success", "articles": key_result})
    
    return build_function_response(show_me_the_shopping_list.__name__, {"status": "no_results", "articles": []})

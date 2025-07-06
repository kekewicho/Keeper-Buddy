from flask import Blueprint, request, current_app
from helpers.dates_helpers import next_paday_key
from helpers.api_helper import db
from itertools import groupby


despensa = Blueprint("despensa", __name__, url_prefix="/despensa")


@despensa.post("/add")
def add_to_shopping_list():

    payload = request.get_json()

    article = payload.get("article")
    payday = payload.get("payday")

    if not article:
        return {"status": "no_article"}, 400
    

    despensa_key = payday or next_paday_key()

    id = db.create_document(
        "despensa",
        {
            "article": article,
            "payday": despensa_key
        }
    )

    if id:

        return {"status": "success", "article": article, "payday": despensa_key}, 200
    
    return {"status": "error"}, 500





@despensa.post("/shoppingList")
def show_me_the_shopping_list():

    payday = request.get_json().get("payday")

    if not payday:

        payday = [next_paday_key()]

    if isinstance(payday, str):
        
        payday = [payday]

    print(payday)

    results = db.filter_documents("despensa", "payday", "in", payday)

    if len(results) == 0:
        return {"status": "no_results", "articles": []}, 200
    

    results = {k:list(v) for k,v in groupby(results, key = lambda x: x["payday"])}
    

    return {"status": "success", "articles": results}, 200


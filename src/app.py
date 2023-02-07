from flask import Flask, request, Response
from config import api_key
import requests
from env import BASEURL, MODEL, TEMPERATUR, MAX_TOKENS
from prompt import create_prompt
import time
import utils
import db
import json 

app = Flask(__name__)
logger = utils.setup_logger()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"



@app.route("/ingredients", methods=["GET"])
def ingredients():
    foods = db.foods()

    result = []

    for food in foods:
        result.append(food.__dict__)
        

    logger.info("Ingredients requested")

    return Response(json.dumps(result), mimetype="application/json")


@app.route("/searchIngredients", methods=["GET"])
def searchIngredients():
    foods = db.foods()

    query = request.args.get("query")

    foods =  utils.where(foods, lambda food: utils.food_search(food, query))

    result = []


    length = foods.__len__()

    logger.info(f"Search Ingredients requested: {query} | {length} results")



    for food in foods:
        result.append(food.__dict__)

    return Response(json.dumps(result), mimetype="application/json")



@app.route(
    "/recipe",
    methods=["POST"],
)
def recipe():
    request_body: dict = request.get_json()
    ingredients = request_body.get("ingredients")
    tools = request_body.get("tools")
    servingAmount = request_body.get("servingAmount")
    targetCalories = request_body.get("targetCalories")
    prompt = create_prompt(ingredients, tools, servingAmount, targetCalories)

    print(prompt)
    logger.info(prompt)


    ### Request Recipte

    data = {
        "model": MODEL,
        "temperature": TEMPERATUR,
        "max_tokens": MAX_TOKENS,
        "prompt": prompt,
        "presence_penalty": 0.0,  # -2.0 to 2.0
        "frequency_penalty": 0.0,  # -2.0 to 2.0
        "stream": False,
    }
    headers = {
        "Content-type": "application/json",
        "Authorization": "Bearer " + api_key,
    }

    start = time.time()

    try:
        response = requests.post(BASEURL, json=data, headers=headers, timeout=45)
    except requests.exceptions.ReadTimeout:
        logger.error("ReadTimeoutError")
    except Exception as e:
        logger.error(e)

    json = response.json()

    if response.status_code != 200:
        print("Error: ", response.status_code)
        print(json["error"])

        return None

    end = time.time()
    duration = end - start

    id = json["id"]
    choice = json["choices"][0]
    finish_reason = choice["finish_reason"]
    answer: str = choice["text"]
    jsonStart = answer.find("{")
    result  = answer[jsonStart:]

    logger.info(f"Returned answer with id={id} duration={utils.time_convert(duration)}")

    if result == None:
        return Response("Error Fetching Response", 500, mimetype="application/json")

    return Response(result, mimetype="application/json")






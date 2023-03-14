from flask import Flask, request, Response
from config import api_key
import requests
from env import BASEURL, MODEL, TEMPERATUR, MAX_TOKENS
from prompt import create_prompt, decode_response_prompt
import time
import utils
import db
import json
from entities.prompt import Difficulty, IngredientSelection
import signal 

app = Flask(__name__)
logger = utils.setup_logger()
limiter = utils.setup_limiter(app)
utils.setup_cors(app)


@app.route("/ping")
@limiter.exempt
def ping():
    return "Pong"


@app.route("/categories", methods=["GET"])
def categories():
    categories = db.categories()
    print(categories)

    logger.info("Categories requested")

    return Response(json.dumps(categories), mimetype="application/json")


@app.route("/ingredients/category", methods=["GET"])
def ingredients_category():
    category = request.args.get("val")

    result = db.getByCategory(category)

    ingredients = []

    for food in result:
        ingredients.append(food.__dict__)

    logger.info("Ingredients by category requested")

    return Response(json.dumps(ingredients), mimetype="application/json")


@app.route("/ingredients", methods=["GET"])
@limiter.limit("5 per second")
def ingredients():
    foods = db.foods()

    result = []

    for food in foods:
        result.append(food.__dict__)

    logger.info("Ingredients requested")

    return Response(json.dumps(result), mimetype="application/json")


@app.route("/searchIngredients", methods=["GET"])
@limiter.limit("5 per second")
def searchIngredients():
    foods = db.foods()

    query = request.args.get("query")
    print(query)
    foods = utils.where(foods, lambda food: utils.food_search(food, query))

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
@limiter.limit("10 per minute")
def recipe():
    request_body: dict = request.get_json()
    # Ingredients
    ingredients = request_body.get("ingredients")
    # Tools
    tools = request_body.get("tools")
    # Serving amount
    servingAmount = request_body.get("servingAmount")
    if servingAmount == None:
        servingAmount = 1
    # Difficulty
    difficulty = Difficulty.from_json(request_body.get("difficulty"))
    # Selection
    selection = IngredientSelection.from_json(request_body.get("selection"))
    if selection is IngredientSelection.RANDOM:
        ingredients = []
    
    # Kitchen
    kitchen = request_body.get("kitchen")
    if kitchen == None:
        kitchen = ""



    prompt = create_prompt(ingredients, tools, servingAmount, difficulty, selection, kitchen)
    logger.info(prompt)
    data = {
        "model": MODEL,
        "temperature": TEMPERATUR,
        "max_tokens": MAX_TOKENS,
        "prompt": prompt,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "stream": False,
    }
    headers = {
        "Content-type": "application/json",
        "Authorization": "Bearer " + api_key,
    }

    start = time.time()
    end = start + 30
    

    while True:
        try:
            logger.info("Requesting OpenAI")
            response = requests.post(BASEURL, json=data, headers=headers, timeout=30)
            if response.status_code != 200:
                raise Exception(
                    f"OpenAI returned status code {response.status_code} with message {response.text}"
                )
            break
        except Exception as e:
            logger.error(e)
            if time.time() >= end:
                return Response(
                    json.dumps({"invalid": True}),
                    500,
                    mimetype="application/json",
                )
            

    json_response = response.json()
    end = time.time()
    duration = end - start

    id = json_response["id"]
    choice = json_response["choices"][0]
    answer: str = choice["text"]

    ### Json Parsing
    result = decode_response_prompt(answer, servingAmount, logger)

    if result == None:
        return Response("Error Fetching Response", 500, mimetype="application/json")

    json_response = json.dumps(result)

    ### Return

    logger.info(f"Returned answer with id={id} duration={utils.time_convert(duration)}")
    logger.info(f"Result: {result}")

    if json_response == None:
        return Response("Error Fetching Response", 500, mimetype="application/json")

    return Response(json_response, mimetype="application/json")

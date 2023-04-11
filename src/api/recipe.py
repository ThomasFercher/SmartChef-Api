import json
import time
import requests 
import utils.utils as utils
from config.env import BASEURL, MODEL, TEMPERATUR, MAX_TOKENS
from service.prompt import create_prompt, decode_response_prompt
from flask import Blueprint, request, Response
from flask_jwt_extended import jwt_required
from utils.limiter import limiter
from utils.logger import logger
from config.config import api_key
from entities.prompt import Difficulty, IngredientSelection




recipe_bp = Blueprint("recipe_bp", __name__)


@recipe_bp.route(
    "/recipe",
    methods=["POST"],
)
@limiter.limit("10 per minute")
#@jwt_required() Will be added when the iOS App implements Authentication
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
 
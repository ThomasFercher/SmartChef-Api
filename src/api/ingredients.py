import json
import utils.utils as utils
import service.db as db
from flask import Blueprint, request, Response
from utils.limiter import limiter
from utils.logger import logger

ingredients_bp = Blueprint("ingredients_bp", __name__)

@ingredients_bp.route("/categories", methods=["GET"])
def categories():
    categories = db.categories()
    print(categories)

    logger.info("Categories requested")

    return Response(json.dumps(categories), mimetype="application/json")


@ingredients_bp.route("/ingredients/category", methods=["GET"])
def ingredients_category():
    category = request.args.get("val")

    result = db.getByCategory(category)

    ingredients = []

    for food in result:
        ingredients.append(food.__dict__)

    logger.info("Ingredients by category requested")

    return Response(json.dumps(ingredients), mimetype="application/json")


@ingredients_bp.route("/ingredients", methods=["GET"])
@limiter.limit("5 per second")
def ingredients():
    foods = db.foods()

    result = []

    for food in foods:
        result.append(food.__dict__)

    logger.info("Ingredients requested")

    return Response(json.dumps(result), mimetype="application/json")


@ingredients_bp.route("/searchIngredients", methods=["GET"])
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
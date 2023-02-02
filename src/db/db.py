import pymongo
from entities.food import Food
from entities.nutrient import Nutrient
from entities.food_nutrient_mapping import FoodNutrientMapping
from env import DATABASE_URL

myclient = pymongo.MongoClient(DATABASE_URL)
db = myclient["smartchef"]
foodTable = db["food"]
nutrientTable = db["nutrient"]
food_nutrient_mapping = db["food_nutrient_mapping"]









def foodNutrientMappings(): 
    result = food_nutrient_mapping.find({})
    mappings = []

    for x in result:
        mapping =  FoodNutrientMapping.from_dict(x)
        mappings.append(mapping)

    return mappings

def nutrients(): 
    result = nutrientTable.find({})
    nutrients = []

    for x in result:
        nutrient =  Nutrient.from_dict(x)
        nutrients.append(nutrient)

    return nutrients



def foods(): 
    result = foodTable.find({})
    foods = []

    for x in result:
        food =  Food.from_dict(x)
        foods.append(food)

    return foods



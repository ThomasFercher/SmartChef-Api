import pymongo
from entities.food import Food
from env import DATABASE_URL

myclient = pymongo.MongoClient(DATABASE_URL)
db = myclient["smartchef"]
foodTable = db["food"]



def foods() -> list[Food]: 
    result = foodTable.find({})
    foods = []

    for x in result:
        food =  Food.from_dict(x)
        foods.append(food)


    

    return foods


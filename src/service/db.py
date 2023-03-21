import pymongo
from entities.food import Food
from entities.user import User
from config.env import DATABASE_URL
from bson import ObjectId


myclient = pymongo.MongoClient(DATABASE_URL)
db = myclient["smartchef"]
foodTable = db["food"]
usersTable = db["users"]



def foods() -> list[Food]: 
    result = foodTable.find({})
    foods = []

    for x in result:
        food =  Food.from_dict(x)
        foods.append(food)

    return foods


def categories() -> list[str]:
    result = foodTable.distinct("Category")
 
    return result

  
def getByCategory(category: str) -> list[Food]:
    result = foodTable.find({"Category": category})
    foods = []

    for x in result:
        food =  Food.from_dict(x)
        foods.append(food)

    return foods


def findUser(email: str) -> User:
    result = usersTable.find_one({"email": email})

    if result is None:
        return None

    return User.from_dict(result)

def findUserById(id: str) -> User:
    result = usersTable.find_one({"_id": ObjectId(id)})

    if result is None:
        return None

    return User.from_dict(result)




def createUser(email: str, password: str) -> str:
    user = User("", email, password, False, False)

    if findUser(email) is not None:
        return "User already exists"
    
    result = usersTable.insert_one(user.to_json(include_id=False))

    if result is None:
        return "Failed to create user"
    
    return "User created successfully"

def deleteUser(id: str) -> bool:
    result = usersTable.delete_one({"_id": ObjectId(id)})
    if result is None:
        return False
    return True
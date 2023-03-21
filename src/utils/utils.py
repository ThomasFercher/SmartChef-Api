from typing import Callable
from entities.food import Food
from flask_cors import CORS
import bcrypt

def setup_cors(app):
    CORS(app)

def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    return "Time Lapsed = {0}:{1}:{2}".format(int(hours), int(mins), sec)







def where(lst: list, condition: Callable[[Food], bool]) -> list[Food]:
    return [x for i, x in enumerate(lst) if condition(x)]


def food_search(food: Food, query: str) -> bool:
    name = food.name.lower()
    query = query.lower()

    return name.__contains__(query)


def encrypt_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed)


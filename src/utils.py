import logging
from typing import Callable
from entities.food import Food

def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  return "Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec)



def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler = logging.FileHandler("logs.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def where(lst: list, condition: Callable[[Food], bool]) -> list[Food]:
    return [x for i,x in enumerate(lst) if condition(x)]


def food_search(food: Food, query: str) -> bool:
    name = food.name.lower()
    query = query.lower()

    return name.__contains__(query)
   

    

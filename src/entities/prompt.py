
from enum import Enum

class Difficulty(Enum):
    EASY = "Beginners"
    MEDIUM = "Intermediates"
    HARD = "Experts"

    @classmethod
    def from_json(cls, json):
        if json == None:
            return Difficulty.HARD
        if json == "Easy":
            return Difficulty.EASY
        if json == "Medium":
            return Difficulty.MEDIUM
        if json == "Hard":
            return Difficulty.HARD
        return Difficulty.HARD
        
        





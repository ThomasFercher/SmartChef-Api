from enum import Enum
class Difficulty(Enum):
    EASY = "Beginner"
    MEDIUM = "Intermediate"
    HARD = "Expert"

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
class IngredientSelection(Enum):
    RANDOM = "Random"
    STRICT = "Strict"
    STRICT_GEN = "StrictGen"
    SEL_GEN = "Selected"

    @classmethod
    def from_json(cls, json):
        if json == None:
            return IngredientSelection.SEL_GEN
        if json == "Strict":
            return IngredientSelection.STRICT
        if json == "StrictGen":
            return IngredientSelection.STRICT_GEN
        if json == "Random":
            return IngredientSelection.RANDOM
        return IngredientSelection.SEL_GEN

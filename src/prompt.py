from logging import Logger
from config import TEMPLATE_PROMPT1,TEMPLATE_PROMPT2
import re
import traceback

def create_prompt( 
    ingredients: list,
    tools: list,
    servingAmount: int = None,
    targetCalories: int = None,
):
    prompt = f"{TEMPLATE_PROMPT1}\nInputIngredients: {', '.join(ingredients)}\nInputTools:{', '.join(tools)}"
    if servingAmount != None:
        prompt += f" \nServingAmount: {servingAmount}"
    # if(targetCalories != None):
    #    prompt += f" \Calories: {targetCalories}"

    prompt +=f"\n{TEMPLATE_PROMPT2}" 

    return prompt


def decode_response_prompt(returned_prompt: str, servingAmount:str, logger:Logger) -> dict:
    s1 = r";(?=[^\[\]]*(?:\[|$))"
    s2 = ";"
    s3 = ":"

    try :
        logger.info(f"Decoding response: {returned_prompt}")
        returned_prompt = returned_prompt.replace("\n", "")

        fields = re.split(s1, returned_prompt)

        if fields.__len__() == 6:
            name = fields[0]
            length_s = fields[1]
            ingredients = fields[3]
            tools = fields[2]
            steps = fields[4]
            tips = fields[5]
        if fields.__len__() == 5:
            firstSplit = fields[0].split(s3)
            name = firstSplit[0]
            length_s = firstSplit[1]
            ingredients = fields[2]
            tools = fields[1]
            steps = fields[3]
            tips = fields[4]
        

        logger.info(f"Decoding response: {name} | {length_s} | {ingredients} | {tools} | {steps} | {tips}")

        ### Name
        name = name.replace("\"", "")

        ### Length
        length = int(length_s)

        ### Ingredients
        ingredients = ingredients.replace("[", "").replace("]", "").replace("{", "").replace("}", "")
        ingredients = ingredients.split(s2)
        dict_ingredients = []
        for ingredient in ingredients:
            ingredient = ingredient.split(s3)
            ingredient_name = ingredient[0]
            amount = ingredient[1]
            dict_ingredients.append({"name": ingredient_name, "amount": amount})

        ### Tools
        tools = tools.replace("[", "").replace("]", "").split(";")
        list_tools = []
        for tool in tools:
            list_tools.append(tool.strip())

        ### Steps
        steps = steps.replace("[", "").replace("]", "").split(";")
        list_steps = []
        for step in steps:
            step = step.split(":")
            if(len(step) == 2):
                list_steps.append(step[1].strip())
        
        

        ### Tips
        tips = tips.replace("[", "").replace("]", "").split(";")
        list_tips = []
        for tip in tips:
            tip = tip.split(":")
            if(len(tip) == 2):
                list_tips.append(tip[1].strip())

        return {
            "name": name,
            "length": length,
            "servingAmount": servingAmount,
            "ingredients": dict_ingredients,
            "tools": list_tools,
            "steps": list_steps,
            "tips": list_tips,
        }

    except Exception as e:
        logger.error(e)
        logger.info(returned_prompt)
        traceback.print_exc()
        return None
    

    

    

from config import TEMPLATE_PROMPT1,TEMPLATE_PROMPT2
import re

def create_prompt( 
    ingredients: list,
    tools: list,
    servingAmount: int = None,
    targetCalories: int = None,
):
    prompt = f"{TEMPLATE_PROMPT1}\nAvailable Ingridients: {', '.join(ingredients)}\nAvailable Tools:{', '.join(tools)}"
    if servingAmount != None:
        prompt += f" \nServing Amount: {servingAmount}"
    # if(targetCalories != None):
    #    prompt += f" \Calories: {targetCalories}"

    prompt +=f"\n{TEMPLATE_PROMPT2}" 

    return prompt


def decode_response_prompt(returned_prompt: str, servingAmount:str) -> dict:
    s1 = r";(?=[^\[\]]*(?:\[|$))"
    s2 = ";"
    s3 = ":"

    

    print(returned_prompt)
    
    returned_prompt = returned_prompt.replace("\n", "")

    fields = re.split(s1, returned_prompt)

    ## print each field
    for field in fields:
        print(field)

    print(fields.__len__())

    name = fields[0]
    length_s = fields[1]
    ingredients = fields[3]
    tools = fields[2]
    steps = fields[4]
    tips = fields[5]

    ### Name
    name = name.replace("\"", "")

    ### Length
    length = int(length_s)

    ### Ingredients
    print(ingredients)
    ingredients = ingredients.replace("[", "").replace("]", "").replace("{", "").replace("}", "")
    print(ingredients)
    ingredients = ingredients.split(s2)
    print("ingredients")
    print(ingredients)
    dict_ingredients = []
    for ingredient in ingredients:
        ingredient = ingredient.split(s3)
        ingredient_name = ingredient[0]
        amount = ingredient[1]
        dict_ingredients.append({"name": ingredient_name, "amount": amount})

    ### Tools
    tools = tools.replace("[", "").replace("]", "").split(";")

    ### Steps
    steps = steps.replace("[", "").replace("]", "").split(";")
    list_steps = []
    for step in steps:
        step = step.split(":")
        list_steps.append(step[1])
     

    ### Tips
    tips = tips.replace("[", "").replace("]", "").split(";")
    list_tips = []
    for tip in tips:
        tip = tip.split(":")
        list_tips.append(tip[1])

    return {
        "name": name,
        "length": length,
        "servingAmount": servingAmount,
        "ingredients": dict_ingredients,
        "tools": tools,
        "steps": list_steps,
        "tips": list_tips,
    }

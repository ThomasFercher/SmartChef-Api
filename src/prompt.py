from config import TEMPLATE_PROMPT1,TEMPLATE_PROMPT2

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


def decode_response_prompt(returned_prompt: str) -> dict:

    s1 = "" #"\u30"
    s2 ="" #"\u31"
   # s3 = "\u27"

    print(returned_prompt)
    
    returned_prompt = returned_prompt.replace("\n", "")
    fields = returned_prompt.split(s1)

    print(fields.__len__())

    name = fields[0]
    length_s = fields[1]
    servingAmount_s = fields[2]
    ingredients = fields[3]
    tools = fields[4]
    steps = fields[5]
    tips = fields[6]

   # print(name)
   # print(length_s)
   # print(servingAmount_s)
    print(ingredients)
    #print(tools)
    #print(steps)
    #print(tips)

    name = name.replace("\"", "")
    length = int(length_s)
    servingAmount = int(servingAmount_s)

    ingredients = ingredients.replace("[", "").replace("]", "").replace("{", "").replace("}", "")

    print(ingredients)
    ingredients = ingredients.split(";")

    print(ingredients)


    json_ingredients = []

    for ingredient in ingredients:
        ingredient = ingredient.split(s2)
        name = ingredient[0]
        amount = ingredient[1]
        json_ingredients.append({"name": name, "amount": amount})


    print(json_ingredients)


    #print(name)

    pass
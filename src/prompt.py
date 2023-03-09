from logging import Logger
from config import PROMPSTART, RULES, UNITS, Format, FormatExample, PROMPTEND
import re
import traceback
from entities.prompt import Difficulty, IngredientSelection


def create_prompt( 
    ingredients: list,
    tools: list,
    servingAmount: int,
    difficulty: Difficulty,
    ingrSel: IngredientSelection
):
    prompt1 = f"{PROMPSTART}{difficulty.value}."
    inputIngredients = f"InputIngredients: {'; '.join(ingredients)}"
    inputTools = f"InputTools: {', '.join(tools)}\n"
    inputServingAmount = f"ServingAmount: {servingAmount}"

    ingredientSelection = getIngredientSelection(ingrSel, ingredients)
    print(ingredientSelection)

    prompt = f"{prompt1}\n{ingredientSelection}{RULES}\n{UNITS}\n{Format}\n{FormatExample}\n\n{inputIngredients}\n{inputTools}\n{inputServingAmount}\n\n{PROMPTEND}"
 
    return prompt


def getIngredientSelection(type: IngredientSelection, ingredients: list):
    start = "Ingredients Selection: "
    end = "Never use InputIngredients which dont fit the recipe. Only use the Selected Ingredients\n"

    genIsMin = True
    maxInput = 2
    additional = 0

    def getMinOrMax():
        if genIsMin:
            return "minimum"
        else:
            return "maximum"

    # switch case:
    if type == IngredientSelection.RANDOM:
        return f"{start}{end}"
    
    if type == IngredientSelection.STRICT:
        maxInput = ingredients.__len__()
        additional = 0
        genIsMin = False
        return f"{start}Never use more than {maxInput} of InputIngredients. {end}"

    if type == IngredientSelection.STRICT_GEN:
        maxInput = ingredients.__len__()
        additional = 8
        genIsMin = True

    if type == IngredientSelection.SEL_GEN:
        maxInput = 2
        additional = 8
        genIsMin = True
   
    return f"{start}Never use more than {maxInput} of the InputIngredients. Always generate a {getMinOrMax()} of {additional} additional Ingredients. {end}"




def decode_response_prompt(returned_prompt: str, servingAmount:str, logger:Logger) -> dict:
    if not returned_prompt.endswith("]"):
        print("not endswith ]")
        returned_prompt = returned_prompt + "]"


    s1 = r";(?=[^\[\]]*(?:\[|$))"
    s2 = ";"
    s3 = ":"
    s4 = "."
    s5 = "\n"

    def splitString(list: str): 
        splitList = list.split(s2)
        if splitList.__len__()> 1:
            print("split by ,")
            return splitList
        
        splitList = list.split(s4)
        if splitList.__len__()> 1:
            print("split by .")
            return splitList
        
        splitList = list.split(s5)
        if splitList.__len__()> 1:
            print("split by \\n")
            return splitList
        
        return splitList
  


    try :
        logger.info(f"Decoding response: {returned_prompt}")
        returned_prompt = returned_prompt.replace("\n", "")

        fields = re.split(s1, returned_prompt)
      
        if fields[-1] == "":
            fields.pop()

        logger.info(f"Decoding response: {fields} length: {fields.__len__()}")
        if fields.__len__() == 6:
            name = fields[0]
            length_s = fields[1]
            ingredients = fields[3]
            tools = fields[2]
            steps = fields[4]
            tips = fields[5]
        elif fields.__len__() == 5:
            firstSplit = fields[0].split(s3)
            name = firstSplit[0]
            length_s = firstSplit[1]
            ingredients = fields[2]
            tools = fields[1]
            steps = fields[3]
            tips = fields[4]
        else:
            logger.info(f"Field Decoding Failed response: {fields}, length: {fields.__len__()}")
            return {
                "invalid": True,
            }


        # remove \" 

        if not length_s.isnumeric(): 
            print("not numeric")
            length_s = re.sub('[^0-9]','', length_s)
        

       

        logger.info(f"Decoding response: {name} | {length_s} | {ingredients} | {tools} | {steps} | {tips}")

        ### Name
        name = name.replace("\"", "").strip()

        ### Length
        length = int(length_s)

        ### Ingredients
        ingredients = ingredients.replace("[", "").replace("]", "").replace("{", "").replace("}", "")
        ingredients = splitString(ingredients)
        dict_ingredients = []
        for ingredient in ingredients:
            ingredient_s = ingredient.split(s3)
            if ingredient_s.__len__() == 1:
                print(", used as separator")
                ingredient_s = ingredient.split(",")
            ingredient_name = ingredient_s[0].strip()

            amount = ""
            if ingredient_s.__len__() > 1:
                amount = ingredient_s[1].strip()
        
            dict_ingredients.append({"name": ingredient_name, "amount": amount})

        ### Tools
        tools = tools.replace("[", "").replace("]", "")
        tools_s = splitString(tools)
        list_tools = []
        for tool in tools_s:
            list_tools.append(tool.strip())

        ### Steps
        steps = steps.replace("[", "").replace("]", "")
        steps_s = splitString(steps)
        list_steps = []
        for step in steps_s:
            step = step.split(s3)
            if(len(step) == 2):
                list_steps.append(step[1].strip())
        
        ### Tips
        tips = tips.replace("[", "").replace("]", "")
        tips_s = splitString(tips)
        list_tips = []
        for tip in tips_s:
            tip = tip.split(s3)
            if(len(tip) == 2):
                list_tips.append(tip[1].strip())


        if list_steps.__len__() == 0:
            logger.info("No steps found in response {returned_prompt}}")
            return {
                "invalid": True,
            }
    


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
    

    


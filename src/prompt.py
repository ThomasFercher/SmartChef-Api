from config import TEMPLATE_PROMPT

def create_prompt( 
    ingredients: list,
    tools: list,
    servingAmount: int = None,
    targetCalories: int = None,
):
    prompt = f"{TEMPLATE_PROMPT}Available Ingridients: {', '.join(ingredients)} \nAvailable Tools: {', '.join(tools)}"
    if servingAmount != None:
        prompt += f" \nServing Amount: {servingAmount}"
    # if(targetCalories != None):
    #    prompt += f" \Calories: {targetCalories}"

    return prompt

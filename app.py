from flask import Flask, request, Response
from config import api_key
import openai



openai.api_key = api_key
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"



@app.route("/recipestream", methods=["POST"], )
def recipe_stream():
    request_body:dict = request.get_json()
    ingredients = request_body.get("ingredients")
    tools =  request_body.get("tools")
    servingAmount = request_body.get("servingAmount")
    targetCalories = request_body.get("targetCalories")
    prompt = create_prompt(ingredients, tools, servingAmount, targetCalories)
    result = request_recipe_stream(prompt)

    if(result == None):
        return Response( "Error Fetching Response", 500,mimetype="application/json")

    return Response(result, mimetype="application/json")


@app.route("/recipe", methods=["POST"], )
def recipe():
    request_body:dict = request.get_json()
    ingredients = request_body.get("ingredients")
    tools =  request_body.get("tools")
    servingAmount = request_body.get("servingAmount")
    targetCalories = request_body.get("targetCalories")
    prompt = create_prompt(ingredients, tools, servingAmount, targetCalories)
    result = request_recipe(prompt)

    if(result == None):
        return Response( "Error Fetching Response", 500,mimetype="application/json")

    return Response(result, mimetype="application/json")

baseUrl = "https://api.openai.com/v1/completions"
model = "text-davinci-003"
temperature = 1
max_tokens = 1000
templatePrompt = """
Create a Cooking recipe with the available Ingredients using the available Tools. Respect the Serving Amount.
Explain every step precisly. 
Tell me the calories of each ingridient.
Add Measurements units to the Ingridient list.
Use both Celcius and Fahrenheit
Output in the following Format: 
{"title": str,
"servingAmount: int,
"ingredients": [{"name": str, "amount": str, "kcal": int}], 
"tools": [""], 
"steps" : [{"number": int, "description": str}], 
"optionalSteps" : [{"number": int, "description": str}],
}
Format the Output correct
"""


def create_prompt(ingredients: list, tools: list, servingAmount: int = None, targetCalories: int = None):
    prompt = f"{templatePrompt}Available Ingridients: {', '.join(ingredients)} \nAvailable Tools: {', '.join(tools)}"
    if(servingAmount != None):
        prompt += f" \nServing Amount: {servingAmount}"
    #if(targetCalories != None):
    #    prompt += f" \Calories: {targetCalories}"

    return prompt

async def request_recipe(prompt: str):
    response = await openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=1000, temperature=temperature, frequency_penalty=0.0, presence_penalty=0.0)
    id = response["id"]
    choice = response["choices"][0]
    finish_reason = choice["finish_reason"]
    answer: str = choice["text"] 
    jsonStart =answer.find("{")
    answer = answer[jsonStart:]
    return answer




def request_recipe_stream(prompt: str):
    answer = ""

    for resp in openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=1000, temperature=temperature, frequency_penalty=0.0, presence_penalty=0.0, stream=True):
        
        data = resp['choices'][0]['text']
        answer += data
        print(data)
     
        



    return answer

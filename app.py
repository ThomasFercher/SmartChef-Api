from flask import Flask, request, Response
from config import api_key
import requests
import db
import logging
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

file_handler = logging.FileHandler("logs.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

app = Flask(__name__)

def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  return "Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route(
    "/recipe",
    methods=["POST"],
)
def recipe():
    request_body: dict = request.get_json()

    ingredients = request_body.get("ingredients")
    tools = request_body.get("tools")
    servingAmount = request_body.get("servingAmount")
    targetCalories = request_body.get("targetCalories")

    print(ingredients)
    print(tools)
    print(servingAmount)
    print(targetCalories)

    prompt = create_prompt(ingredients, tools, servingAmount, targetCalories)

    print(prompt)

    result = request_recipe(prompt)

    if result == None:
        return Response("Error Fetching Response", 500, mimetype="application/json")

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


def create_prompt(
    ingredients: list,
    tools: list,
    servingAmount: int = None,
    targetCalories: int = None,
):
    prompt = f"{templatePrompt}Available Ingridients: {', '.join(ingredients)} \nAvailable Tools: {', '.join(tools)}"
    if servingAmount != None:
        prompt += f" \nServing Amount: {servingAmount}"
    # if(targetCalories != None):
    #    prompt += f" \Calories: {targetCalories}"

    return prompt


def request_recipe(prompt: str):

    data = {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "prompt": prompt,
        "presence_penalty": 0.0,  # -2.0 to 2.0
        "frequency_penalty": 0.0,  # -2.0 to 2.0
        "stream": False,
    }
    headers = {
        "Content-type": "application/json",
        "Authorization": "Bearer " + api_key,
    }

    start = time.time()

    try:
        response = requests.post(baseUrl, json=data, headers=headers, timeout=45)
    except requests.exceptions.ReadTimeout:
        logger.error("ReadTimeoutError")
    except Exception as e:
        logger.error(e)

    json = response.json()

    if response.status_code != 200:
        print("Error: ", response.status_code)
        print(json["error"])

        return None

    end  = time.time()
    duration = end - start

    id = json["id"]
    choice = json["choices"][0]
    finish_reason = choice["finish_reason"]
    answer: str = choice["text"]
    jsonStart = answer.find("{")
    answer = answer[jsonStart:]

    logger.info(f"Returned answer with id={id} duration={time_convert(duration)}")

    return answer

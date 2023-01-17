from flask import Flask, request
import requests


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/recipe", methods=["POST"])
def recipe():
    request_body = request.get_json()
    
    ingredients = request_body["ingredients"]
    tools = request_body["tools"]

    print(ingredients)
    print(tools)

    prompt = create_prompt(ingredients, tools)

    print(prompt)

    return request_recipe(prompt)


apiKey = "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"
baseUrl = "https://api.openai.com/v1/completions"
model = "text-davinci-003"
temperature = 1
max_tokens = 1000
templatePrompt = """
Create a Cooking recipe with the available Ingredients using the available Tools.
Explain every step precisly.
Add Measurements units to the Ingridient list.
Use both Celcius and Fahrenheit.
Output only JSON using the following Format: {\"title\": \"title of recipe\",\"ingridients\": [\"ingridient1\", \"ingridient2\"], \"steps\" : [  \"1\": \"step1 description\", \"2\": \"step2 description\"], \"sidenotes\": \"notes\"}
"""


def create_prompt(ingredients: list, tools: list):
   

    return f"{templatePrompt} \nAvailable Ingridients: {', '.join(ingredients)} \nAvailable Tools: {', '.join(tools)}"

def request_recipe(prompt: str):

    data = {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "prompt": prompt,
    }
    headers = {
        "Content-type": "application/json",
        "Authorization": "Bearer " + apiKey,
    }

    response = requests.post(baseUrl, json=data, headers=headers)


    json = response.json() 



    id = json["id"]
    
    choice = json["choices"][0]

    finish_reason = choice["finish_reason"]
    answer = choice["text"]

    print("id: ", id)
    print("finish_reason: ", finish_reason)

    return answer

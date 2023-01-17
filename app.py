from flask import Flask, request, Response
import requests


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/recipe", methods=["POST"], )
def recipe():
    request_body = request.get_json()
    
    ingredients = request_body["ingredients"]
    tools = request_body["tools"]

    print(ingredients)
    print(tools)

    prompt = create_prompt(ingredients, tools)

    
    result = request_recipe(prompt)

    if(result == None):
        return "Error Fetching Response", 500

    return Response(result, mimetype="application/json")


apiKey = "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"
baseUrl = "https://api.openai.com/v1/completions"
model = "text-davinci-003"
temperature = 0.5
max_tokens = 500
templatePrompt = """
Create a Cooking recipe with the available Ingredients using the available Tools.
Explain every step precisly.
Add Measurements units to the Ingridient list.
Use both Celcius and Fahrenheit.
Output only JSON using the following Format: {\"title\": \"title of recipe\",\"ingridients\": [\"ingridient1\", \"ingridient2\"], \"tools\": [\"tool1\", \"tool2\"] ,\"steps\" : [  \"1\": \"step1 description\", \"2\": \"step2 description\"], \"sidenotes\": \"notes\"}
Format the Output correct
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

    response = requests.post(baseUrl, json=data, headers=headers, timeout=20)
  
    json = response.json() 

    if(response.status_code != 200):
        print("Error: ", response.status_code)
        print(json["error"])
        
        return None

    id = json["id"]
    choice = json["choices"][0]
    finish_reason = choice["finish_reason"]
    answer: str = choice["text"] 
    jsonStart =answer.find("{")
    answer = answer[jsonStart:]




    print("id: ", id)
    print("finish_reason: ", finish_reason)

    return answer





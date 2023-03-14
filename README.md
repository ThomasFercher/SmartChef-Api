# SmartChef Api
Rest Api using Flask and OpenAi Api.

# Requests


## Generate Recipe

`POST /recipe`

> ## Difficulty: 
> - Easy
> - Medium
> - Hard

> ## Selection:
> - Random: Random Ingredients are selected. The List of ingredients is ignored.
> - Strict: Only the given ingredients are used.
> - StrictGen: All the given ingredients are used and a few ingredients are generated.
> - Selected: Fitting Ingredients are selected and others are generated.

> ## Kitchen:
> The type of kitchen the recipe should originate from. \
> Examples:
> - Japanese
> - Italian
> - British
> - Indian
> - African


### Body
```
{
    "ingredients": [
        "Pasta, raw",
        "Parmesan",
        "Tomato",
        "Cocaine",
        "Snake"
    ],
    "tools": [],
    "servingAmount": 1,
    "difficulty": "Hard",
    "selection": "Selected",
    "kitchen": ""
}
```

### Response
```
{
    "name": "Cheesy Pasta with Tomatoes",
    "length": 30,
    "servingAmount": 1,
    "ingredients": [
        {
            "name": "Pasta",
            "amount": "100g"
        },
        {
            "name": "Parmesan",
            "amount": "100g"
        },
        {
            "name": "Tomato",
            "amount": "1"
        },
        {
            "name": "Garlic",
            "amount": "1 clove"
        },
    ],
    "tools": [
        "Pot",
        "Stove"
    ],
    "steps": [
        "Bring a pot of salted water to a boil",
        "Cook the pasta according to the package instructions",
    ],
    "tips": [
        "Add more or less red pepper flakes according to your spice preference",
        "If desired, you can add a sprinkle of crushed almonds for extra texture and flavor."
    ]
}
```


## /ingredients

## /categories





# Debug
To Start: flask --app app run 
To Debug: flask --app app --debug run 
nohup gunicorn --bind 0.0.0.0:8000 --workers 4 --threads 4 wsgi:app &

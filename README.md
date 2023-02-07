# SmartChef Api
Rest Api using Flask and OpenAi Api.

# Requirements
Python3 

git clone 
cd 
python3 -m venv venv
. venv/bin/activate 


## Dependencies
Flask
requests
pymongo

install with pip install



To Start: flask --app app run 

To Debug: flask --app app --debug run 

# Requests

## Post /recipe

Start Command: 
nohup gunicorn --bind 0.0.0.0:8000 --workers 4 --threads 4 wsgi:app &


https://bartsimons.me/gunicorn-as-a-systemd-service/
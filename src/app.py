from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required

import utils.utils as utils

from utils.limiter import limiter, blacklist
from api.ingredients import ingredients_bp 
from api.recipe import recipe_bp
from api.authentication import auth_bp

from config.config import SECRET_KEY


### Init
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)
limiter.init_app(app)
utils.setup_cors(app)


### Routes
app.register_blueprint(ingredients_bp)
app.register_blueprint(recipe_bp)
app.register_blueprint(auth_bp)

### Standard routes
@app.route("/ping")
@limiter.exempt
def ping():
    return "Pong"

  
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(_,decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist




import os

from flask import send_file
from catalog import app, client_path

#create API end points
from catalog.core import api_manager
from catalog.authentication.models import *

for model_name in app.config['API_MODELS']:
    model_class = app.config['API_MODELS'][model_name]
    api_manager.create_api(model_class, methods=['GET', 'POST'])


# Routes

@app.route('/')
def index():
    return send_file(os.path.join(client_path, 'index.html'))





    


# Import flask and template operators
from flask import Flask, request, Response
from flask import render_template, send_from_directory, url_for

# Define the WSGI application object
import os
current_path = os.path.dirname(__file__)
client_path = os.path.abspath(os.path.join(current_path, 'static'))

app = Flask(__name__, static_url_path='', static_folder=client_path)

# Configurations
app.config.from_object('config')
#app.config['UPLOAD_FOLDER'] = 'files'

import catalog.core
import catalog.controllers

# Import a module / component using its blueprint handler variable (authentication)
from catalog.authentication.controllers import authentication as auth_module

# Register blueprint(s)
app.register_blueprint(auth_module)

# Build the database:
# This will create the database file using SQLAlchemy
#db.create_all()
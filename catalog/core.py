from catalog import app

from flask.ext.sqlalchemy import SQLAlchemy

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
db = SQLAlchemy(app)

from MAPS import routes

from MAPS.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')

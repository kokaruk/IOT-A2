from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)



# last import
from app import routes
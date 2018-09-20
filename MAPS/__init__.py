from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

# do not delete these two lines ever! optimiser complains but ignore it
from MAPS.api import bp as api_bp
from MAPS import routes, models

app.register_blueprint(api_bp, url_prefix='/api')

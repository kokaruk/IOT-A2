from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

import logging
import os
from logging.handlers import RotatingFileHandler
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

# do not delete these two lines ever! optimiser complains but ignore it
from MAPS.api import bp as api_bp
from MAPS import routes, models, errors


if not app.debug:
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)
    file_handler = RotatingFileHandler(f'{logs_dir}/maps.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')



app.register_blueprint(api_bp, url_prefix='/api')

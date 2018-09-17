import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
    CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')
    CLOUDSQL_DATABASE = os.environ.get('CLOUDSQL_DATABASE')
    CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
    # The CloudSQL proxy is used locally to connect to the cloudsql instance.
    # To start the proxy, use:
    #
    #   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
    #
    # Port 3306 is the standard MySQL port. If you need to use a different port,
    # change the 3306 to a different port number.

    # When running on App Engine a unix socket is used to connect to the cloudsql
    # instance.
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(
        CLOUDSQL_USER, CLOUDSQL_PASSWORD, CLOUDSQL_CONNECTION_NAME, CLOUDSQL_DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

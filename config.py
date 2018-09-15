import os

SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'

# REFERENCE: https://github.com/GoogleCloudPlatform/getting-started-python/blob/master/4-auth/config.py
PROJECT_ID = 'iot-demo-calvin'
DATA_BACKEND = 'cloudsql'
CLOUDSQL_USER = 'iot-ass-2'
CLOUDSQL_PASSWORD = 'iot-password'
# CLOUDSQL_DATABASE = 'maps'
CLOUDSQL_DATABASE = 'test'
CLOUDSQL_CONNECTION_NAME = 'iot-demo-calvin:australia-southeast1:mysql-demo'
# The CloudSQL proxy is used locally to connect to the cloudsql instance.
# To start the proxy, use:
#
#   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
#
# Port 3306 is the standard MySQL port. If you need to use a different port,
# change the 3306 to a different port number.

# When running on App Engine a unix socket is used to connect to the cloudsql
# instance.
LIVE_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@localhost/{database}'
    '?unix_socket=/cloudsql/{connection_name}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)


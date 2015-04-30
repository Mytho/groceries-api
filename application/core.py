from os import environ
from flask import Flask

from application.views import login
from application.errors import init_errors
from application.models import init_models


app = Flask(__name__)
app.config.setdefault('SQLALCHEMY_DATABASE_URI', environ.get('DATABASE_URL'))

init_errors(app)
init_models(app)

routes = {'/login': login}

for endpoint, func in routes.iteritems():
    app.add_url_rule(endpoint, view_func=func)

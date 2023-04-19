from flask import Flask

from config import Config

from .api.routes import api
from .stripe.routes import stripe

from .models import db

from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r"/*": {"origins": "*"}})

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(api)
app.register_blueprint(stripe)

from . import routes
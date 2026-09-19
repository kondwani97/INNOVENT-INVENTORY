from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Extensions are created here (uninitialized) so models and app.py
# can both import the same instance without circular imports.
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
jwt = JWTManager()
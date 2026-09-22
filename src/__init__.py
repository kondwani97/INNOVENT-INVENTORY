from flask import Flask

from src.config.config import Config
from src.extensions import db, migrate, cors, jwt


def create_app():
    """Application factory: builds and configures the Flask app."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Bind extensions to this app instance
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    from src.routes.roles import roles_bp
    app.register_blueprint(roles_bp)
    
    from src.routes.businesses import businesses_bp
    app.register_blueprint(businesses_bp)
    
    from src.routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    from src.routes.categories import categories_bp
    app.register_blueprint(categories_bp)

    # Import models so Flask-Migrate can detect them
    from src.models import role  # noqa: F401

    @app.route("/health")
    def health_check():
        return {"status": "ok", "service": "innovent-api"}

    return app

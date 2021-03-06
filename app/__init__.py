from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()


#Application Factory Pattern
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'You do not have access to this page. Login first please!'
    login_manager.login_message_category = 'warning'

    from app.blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)


    from app.blueprints.api import bp as api_bp
    app.register_blueprint(api_bp)

    # Needs app context
    with app.app_context():
        # from .import context_processors

        from app.blueprints.shop import bp as shop_bp
        app.register_blueprint(shop_bp)
        # from app import views
    
    from app import views, models

    return app
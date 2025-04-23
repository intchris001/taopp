from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    from app.routes import main, auth, product, cart, order
    app.register_blueprint(main.main_bp)
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(product.product_bp)
    app.register_blueprint(cart.cart_bp)
    app.register_blueprint(order.order_bp)

    @login_manager.user_loader
    def load_user(id):
        from app.models.user import User
        return User.query.get(int(id))

    @app.context_processor
    def inject_cart_count():
        if hasattr(login_manager, 'current_user') and login_manager.current_user.is_authenticated:
            cart = login_manager.current_user.cart
            return {'cart_count': cart.item_count if cart else 0}
        return {'cart_count': 0}

    return app

from app import models 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object('app.config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    # Registra as rotas
    from app.routes.auth import auth_bp
    from app.routes.contato import contato_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(contato_bp)
    app.register_blueprint(admin_bp)

    return app
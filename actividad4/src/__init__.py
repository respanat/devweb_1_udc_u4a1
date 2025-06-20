from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
mail = Mail()


def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    db.init_app(app)
    mail.init_app(app)

    from .models.entities import usuario
    from .models.entities import computador

    with app.app_context():
        db.create_all()

    from .models.repositories.usuario_repository import UsuarioRepository
    from .models.repositories.computador_repository import ComputadorRepository
    from .models.services.usuario_service import UsuarioService
    from .models.services.computador_service import ComputadorService
    from .models.services.email_service import EmailService

    email_service_instance = EmailService(mail)

    usuario_service_instance = UsuarioService(UsuarioRepository, email_service_instance)

    computador_service_instance = ComputadorService(ComputadorRepository)

    app.usuario_service = usuario_service_instance
    app.computador_service = computador_service_instance
    app.email_service = email_service_instance

    return app


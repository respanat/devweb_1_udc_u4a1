from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
mail = Mail()


def create_app():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    app = Flask(__name__, template_folder=os.path.join(base_dir, 'templates'))

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
    from .controllers.computador_controller import computador_bp
    from .controllers.usuario_controller import usuario_bp

    email_service_instance = EmailService(mail)

    usuario_service_instance = UsuarioService(
        UsuarioRepository, email_service_instance)

    computador_service_instance = ComputadorService(ComputadorRepository)

    app.usuario_service = usuario_service_instance
    app.computador_service = computador_service_instance
    app.email_service = email_service_instance
    app.register_blueprint(computador_bp)
    app.register_blueprint(usuario_bp)

    @app.route('/')
    def redirigir_al_login():
        return redirect(url_for('usuario_bp.mostrar_formulario_login'))
    return app

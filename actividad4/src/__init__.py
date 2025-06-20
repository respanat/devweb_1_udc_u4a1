from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv


load_dotenv()


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY', 'una_clave_secreta_por_defecto_muy_segura')
    app.config["DEBUG"] = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't') # Convierte string a booleano

    # Configuración de la Base de Datos
    db_url = os.getenv("DATABASE_URL", "mysql+mysqlconnector://ramiro_espana:AbcdeUdeC@localhost:3306/act4_devweb")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Recomendado para evitar warnings y consumo de memoria

    # Inicializar la instancia de SQLAlchemy con la aplicación Flask
    db.init_app(app)

    from .models.entities import usuario # Importa el modelo Usuario

    # Crear las tablas de la base de datos (si no existen) dentro de un contexto de la aplicación.
    with app.app_context():
        db.create_all()

    return app

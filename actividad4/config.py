import os
from dotenv import load_dotenv

load_dotenv() # Carga las variables de entorno del archivo .env

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'Cl4v3_53cr374_D3_D354rr0ll0')
    DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't') # Modo depuración

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+mysqlconnector://ramiro_espana:AbcdeUdeC@localhost:3306/act3_devweb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Deshabilita el seguimiento de modificaciones de objetos de SQLAlchemy.

    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ('true', '1', 't')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'desarolloappudc@gmail.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'fdtl hacv ohhn bqja')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'desarolloappudc@gmail.com')

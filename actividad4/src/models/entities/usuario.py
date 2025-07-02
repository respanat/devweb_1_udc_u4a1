from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from src import db


class Usuario(db.Model):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    username: Mapped[str] = mapped_column(
        String(80), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    nombre: Mapped[str] = mapped_column(String(120), nullable=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    def __init__(self, username, password, nombre, email, id=None):
        self.username = username
        self.password = password
        self.nombre = nombre
        self.email = email
        if id is not None:
            self.id = id

    def __repr__(self):
        return f"<Usuario(id={self.id}, username='{self.username}', nombre='{self.nombre}', email='{self.email}')>"

from src import db
from src.models.entities.usuario import Usuario
from typing import Optional


class UsuarioRepository:
    @staticmethod
    def find_all() -> list[Usuario]:
        return db.session.execute(db.select(Usuario)).scalars().all()

    @staticmethod
    def find_by_id(id: int) -> Optional[Usuario]:
        return db.session.get(Usuario, id)

    @staticmethod
    def save(usuario: Usuario) -> Usuario:
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def delete(usuario: Usuario):
        db.session.delete(usuario)
        db.session.commit()

    @staticmethod
    def find_by_username(username: str) -> Optional[Usuario]:
        return db.session.execute(db.select(Usuario).filter_by(username=username)).scalar_one_or_none()

    @staticmethod
    def find_by_email(email: str) -> Optional[Usuario]:
        return db.session.execute(db.select(Usuario).filter_by(email=email)).scalar_one_or_none()

    @staticmethod
    def exists_by_username(username: str) -> bool:
        return db.session.query(Usuario).filter_by(username=username).first() is not None

    @staticmethod
    def exists_by_email(email: str) -> bool:
        return db.session.query(Usuario).filter_by(email=email).first() is not None

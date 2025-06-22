from typing import List, Optional

from src.models.entities.usuario import Usuario
from src.models.repositories.usuario_repository import UsuarioRepository
from src.models.services.email_service import EmailService


class UsuarioService:
    def __init__(
        self, usuario_repository: UsuarioRepository, email_service: EmailService
    ):
        self.usuario_repository = usuario_repository
        self.email_service = email_service

    def crear_usuario(self, usuario: Usuario) -> Usuario:
        return self.usuario_repository.save(usuario)

    def obtener_usuario_por_id(self, id: int) -> Optional[Usuario]:
        return self.usuario_repository.find_by_id(id)

    def obtener_todos_los_usuarios(self) -> List[Usuario]:
        return self.usuario_repository.find_all()

    def actualizar_usuario(self, usuario: Usuario) -> Usuario:
        return self.usuario_repository.save(usuario)

    def eliminar_usuario(self, id: int):
        usuario_a_eliminar = self.usuario_repository.find_by_id(id)
        if usuario_a_eliminar:
            self.usuario_repository.delete(usuario_a_eliminar)
        else:
            print(
                f"Advertencia: No se encontró usuario con ID {id} para eliminar."
            )

    def obtener_usuario_por_username(self, username: str) -> Optional[Usuario]:
        return self.usuario_repository.find_by_username(username)

    def autenticar_usuario(
        self, username_or_email: str, password: str
    ) -> Optional[Usuario]:
        usuario = self.usuario_repository.find_by_username(username_or_email)
        if not usuario:
            usuario = self.usuario_repository.find_by_email(username_or_email)

        if usuario and usuario.password == password:
            return usuario
        return None

    def iniciar_recordar_password(self, identifier: str) -> Optional[Usuario]:
        usuario = self.usuario_repository.find_by_username(identifier)
        if not usuario:
            usuario = self.usuario_repository.find_by_email(identifier)
        return usuario

    def send_password_recovery_email(self, usuario: Usuario):
        subject = "Recuperación de Contraseña"
        body = (
            f"Hola {usuario.nombre},\n\n"
            f"Tu contraseña es: {usuario.password}\n\n"
            "Por favor, no compartas esta información con nadie.\n\n"
            "Saludos,\nTu Equipo de Soporte"
        )
        self.email_service.send_simple_mail(usuario.email, subject, body)


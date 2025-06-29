import unittest
from unittest.mock import MagicMock, patch
import logging

from src.models.entities.usuario import Usuario
from src.models.repositories.usuario_repository import UsuarioRepository
from src.models.services.usuario_service import UsuarioService
from src.models.services.email_service import EmailService


class TestUsuario(unittest.TestCase):
    def test_creacion_usuario(self):
        usuario = Usuario(
            username="prueba",
            password="prueba_clave",
            nombre="Usuario de Prueba",
            email="prueba@udc.com",
            id=1
        )

        self.assertEqual(usuario.username, "prueba")
        self.assertEqual(usuario.password, "prueba_clave")
        self.assertEqual(usuario.nombre, "Usuario de Prueba")
        self.assertEqual(usuario.email, "prueba@udc.com")
        self.assertEqual(usuario.id, 1)
        self.assertIn("prueba", repr(usuario))
        self.assertIn("Usuario de Prueba", repr(usuario))


class TestUsuarioRepository(unittest.TestCase):
    @patch('src.db.session')
    def test_find_all(self, mock_db_session):
        mock_usuario1 = Usuario("prueba1", "clave1", "Nombre Uno", "prueba1@udc.com", 1)
        mock_usuario2 = Usuario("prueba2", "clave2", "Nombre Dos", "prueba2@udc.com", 2)
        
        mock_db_session.execute.return_value.scalars.return_value.all.return_value = [
            mock_usuario1,
            mock_usuario2,
        ]

        usuarios = UsuarioRepository.find_all()
        self.assertEqual(len(usuarios), 2)
        self.assertEqual(usuarios[0].username, "prueba1")
        self.assertEqual(usuarios[1].nombre, "Nombre Dos")
        mock_db_session.execute.assert_called_once()

    @patch('src.db.session')
    def test_find_by_id(self, mock_db_session):
        mock_usuario = Usuario("prueba_find", "clave_find", "Usuario Find", "find@udc.com", 5)
        mock_db_session.get.return_value = mock_usuario

        usuario_encontrado = UsuarioRepository.find_by_id(5)
        self.assertIsNotNone(usuario_encontrado)
        self.assertEqual(usuario_encontrado.id, 5)
        self.assertEqual(usuario_encontrado.username, "prueba_find")
        mock_db_session.get.assert_called_once_with(Usuario, 5)

    @patch('src.db.session')
    def test_save_new_usuario(self, mock_db_session):
        nuevo_usuario = Usuario("prueba_nuevo", "clave_nuevo", "Usuario Nuevo", "nuevo@udc.com")
        
        mock_db_session.add.return_value = None
        mock_db_session.commit.return_value = None
        
        resultado = UsuarioRepository.save(nuevo_usuario)
        
        mock_db_session.add.assert_called_once_with(nuevo_usuario)
        mock_db_session.commit.assert_called_once()
        self.assertEqual(resultado, nuevo_usuario)

    @patch('src.db.session')
    def test_delete_usuario(self, mock_db_session):
        usuario_a_eliminar = Usuario("prueba_eliminar", "clave_eliminar", "Usuario Eliminar", "eliminar@udc.com", 99)
        
        UsuarioRepository.delete(usuario_a_eliminar)
        
        mock_db_session.delete.assert_called_once_with(usuario_a_eliminar)
        mock_db_session.commit.assert_called_once()

    @patch('src.db.session')
    def test_find_by_username(self, mock_db_session):
        mock_usuario = Usuario("prueba_spec", "clave_spec", "Usuario Especifico", "spec@udc.com", 10)
        
        mock_execute_result = MagicMock()
        mock_execute_result.scalar_one_or_none.return_value = mock_usuario
        mock_db_session.execute.return_value = mock_execute_result

        usuario_encontrado = UsuarioRepository.find_by_username("prueba_spec")
        self.assertIsNotNone(usuario_encontrado)
        self.assertEqual(usuario_encontrado.username, "prueba_spec")
        mock_db_session.execute.assert_called_once()

    @patch('src.db.session')
    def test_find_by_email(self, mock_db_session):
        mock_usuario = Usuario("prueba_email", "clave_email", "Usuario Email", "email@udc.com", 11)
        
        mock_execute_result = MagicMock()
        mock_execute_result.scalar_one_or_none.return_value = mock_usuario
        mock_db_session.execute.return_value = mock_execute_result

        usuario_encontrado = UsuarioRepository.find_by_email("email@udc.com")
        self.assertIsNotNone(usuario_encontrado)
        self.assertEqual(usuario_encontrado.email, "email@udc.com")
        mock_db_session.execute.assert_called_once()

    @patch('src.db.session')
    def test_exists_by_username(self, mock_db_session):
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = Usuario("existe", "pass", "Existe", "existe@udc.com")
        self.assertTrue(UsuarioRepository.exists_by_username("existe"))
        mock_db_session.query.assert_called_once_with(Usuario)
        mock_db_session.query.return_value.filter_by.assert_called_once_with(username="existe")

    @patch('src.db.session')
    def test_exists_by_username_not_found(self, mock_db_session):
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = None
        self.assertFalse(UsuarioRepository.exists_by_username("no_existe"))

    @patch('src.db.session')
    def test_exists_by_email(self, mock_db_session):
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = Usuario("usuario", "pass", "Usuario", "email_existe@udc.com")
        self.assertTrue(UsuarioRepository.exists_by_email("email_existe@udc.com"))

    @patch('src.db.session')
    def test_exists_by_email_not_found(self, mock_db_session):
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = None
        self.assertFalse(UsuarioRepository.exists_by_email("email_no_existe@udc.com"))


class TestUsuarioService(unittest.TestCase):
    def setUp(self):
        self.mock_usuario_repository = MagicMock(spec=UsuarioRepository)
        self.mock_email_service = MagicMock(spec=EmailService)
        self.usuario_service = UsuarioService(
            self.mock_usuario_repository, self.mock_email_service
        )
        self.dummy_usuario = Usuario(
            username="prueba",
            password="prueba_clave",
            nombre="Usuario de Prueba",
            email="prueba@udc.com",
            id=1
        )

    def test_crear_usuario(self):
        self.mock_usuario_repository.save.return_value = self.dummy_usuario
        usuario_creado = self.usuario_service.crear_usuario(self.dummy_usuario)
        self.assertIsNotNone(usuario_creado)
        self.assertEqual(usuario_creado.username, self.dummy_usuario.username)
        self.mock_usuario_repository.save.assert_called_once_with(self.dummy_usuario)

    def test_obtener_usuario_por_id(self):
        self.mock_usuario_repository.find_by_id.return_value = self.dummy_usuario
        usuario = self.usuario_service.obtener_usuario_por_id(1)
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.id, 1)
        self.mock_usuario_repository.find_by_id.assert_called_once_with(1)

    def test_obtener_todos_los_usuarios(self):
        self.mock_usuario_repository.find_all.return_value = [self.dummy_usuario]
        usuarios = self.usuario_service.obtener_todos_los_usuarios()
        self.assertEqual(len(usuarios), 1)
        self.mock_usuario_repository.find_all.assert_called_once()

    def test_actualizar_usuario(self):
        self.mock_usuario_repository.save.return_value = self.dummy_usuario
        usuario_actualizado = self.usuario_service.actualizar_usuario(self.dummy_usuario)
        self.assertIsNotNone(usuario_actualizado)
        self.mock_usuario_repository.save.assert_called_once_with(self.dummy_usuario)

    def test_eliminar_usuario_existente(self):
        self.mock_usuario_repository.find_by_id.return_value = self.dummy_usuario
        self.usuario_service.eliminar_usuario(1)
        self.mock_usuario_repository.find_by_id.assert_called_once_with(1)
        self.mock_usuario_repository.delete.assert_called_once_with(self.dummy_usuario)

    def test_eliminar_usuario_no_existente(self):
        self.mock_usuario_repository.find_by_id.return_value = None
        
        with self.assertLogs('src.models.services.usuario_service', level='WARNING') as cm:
             self.usuario_service.eliminar_usuario(999)
             self.assertEqual(len(cm.output), 1)
             self.assertIn("Advertencia: No se encontró usuario con ID 999 para eliminar.", cm.output[0])
        
        self.mock_usuario_repository.find_by_id.assert_called_once_with(999)
        self.mock_usuario_repository.delete.assert_not_called()

    def test_obtener_usuario_por_username(self):
        self.mock_usuario_repository.find_by_username.return_value = self.dummy_usuario
        usuario = self.usuario_service.obtener_usuario_por_username("prueba")
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.username, "prueba")
        self.mock_usuario_repository.find_by_username.assert_called_once_with("prueba")

    def test_autenticar_usuario_por_username(self):
        self.mock_usuario_repository.find_by_username.return_value = self.dummy_usuario
        self.mock_usuario_repository.find_by_email.return_value = None

        usuario_autenticado = self.usuario_service.autenticar_usuario(
            "prueba", "prueba_clave"
        )
        self.assertIsNotNone(usuario_autenticado)
        self.assertEqual(usuario_autenticado.username, "prueba")
        self.mock_usuario_repository.find_by_username.assert_called_once_with("prueba")
        self.mock_usuario_repository.find_by_email.assert_not_called()

    def test_autenticar_usuario_por_email(self):
        self.mock_usuario_repository.find_by_username.return_value = None
        self.mock_usuario_repository.find_by_email.return_value = self.dummy_usuario

        usuario_autenticado = self.usuario_service.autenticar_usuario(
            "prueba@udc.com", "prueba_clave"
        )
        self.assertIsNotNone(usuario_autenticado)
        self.assertEqual(usuario_autenticado.email, "prueba@udc.com")
        self.mock_usuario_repository.find_by_username.assert_called_once_with("prueba@udc.com")
        self.mock_usuario_repository.find_by_email.assert_called_once_with("prueba@udc.com")

    def test_autenticar_usuario_credenciales_invalidas(self):
        self.mock_usuario_repository.find_by_username.return_value = None
        self.mock_usuario_repository.find_by_email.return_value = None

        usuario_autenticado = self.usuario_service.autenticar_usuario(
            "no_existe", "clave_incorrecta"
        )
        self.assertIsNone(usuario_autenticado)
        self.mock_usuario_repository.find_by_username.assert_called_once_with("no_existe")
        self.mock_usuario_repository.find_by_email.assert_called_once_with("no_existe")

    def test_iniciar_recordar_password_username(self):
        self.mock_usuario_repository.find_by_username.return_value = self.dummy_usuario
        self.mock_usuario_repository.find_by_email.return_value = None

        usuario = self.usuario_service.iniciar_recordar_password("prueba")
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.username, "prueba")
        self.mock_usuario_repository.find_by_username.assert_called_once_with("prueba")
        self.mock_usuario_repository.find_by_email.assert_not_called()

    def test_iniciar_recordar_password_email(self):
        self.mock_usuario_repository.find_by_username.return_value = None
        self.mock_usuario_repository.find_by_email.return_value = self.dummy_usuario

        usuario = self.usuario_service.iniciar_recordar_password("prueba@udc.com")
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.email, "prueba@udc.com")
        self.mock_usuario_repository.find_by_username.assert_called_once_with("prueba@udc.com")
        self.mock_usuario_repository.find_by_email.assert_called_once_with("prueba@udc.com")

    def test_iniciar_recordar_password_no_encontrado(self):
        self.mock_usuario_repository.find_by_username.return_value = None
        self.mock_usuario_repository.find_by_email.return_value = None

        usuario = self.usuario_service.iniciar_recordar_password("no_existe")
        self.assertIsNone(usuario)
        self.mock_usuario_repository.find_by_username.assert_called_once_with("no_existe")
        self.mock_usuario_repository.find_by_email.assert_called_once_with("no_existe")

    def test_send_password_recovery_email(self):
        self.usuario_service.send_password_recovery_email(self.dummy_usuario)
        
        expected_subject = "Recuperación de Contraseña"
        expected_body_part1 = f"Hola {self.dummy_usuario.nombre},\n\nTu contraseña es: {self.dummy_usuario.password}"
        expected_body_part2 = "Por favor, no compartas esta información con nadie.\n\nSaludos,\nTu Equipo de Soporte"
        
        self.mock_email_service.send_simple_mail.assert_called_once()
        args, kwargs = self.mock_email_service.send_simple_mail.call_args
        
        self.assertEqual(args[0], self.dummy_usuario.email)
        self.assertEqual(args[1], expected_subject)
        self.assertIn(expected_body_part1, args[2])
        self.assertIn(expected_body_part2, args[2])


if __name__ == '__main__':
    unittest.main()

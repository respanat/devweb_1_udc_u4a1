import unittest
from unittest.mock import MagicMock, patch

from src.models.entities.computador import Computador
from src.models.repositories.computador_repository import ComputadorRepository
from src.models.services.computador_service import ComputadorService

class TestComputador(unittest.TestCase):
    """
    Pruebas unitarias para la entidad Computador.
    """

    def test_creacion_computador(self):
        """
        Verifica que una instancia de Computador se cree correctamente
        con todos sus atributos.
        """
        computador = Computador(
            marca="Dell",
            categoria="Portátil",
            marca_cpu="Intel",
            velocidad_cpu=2.5,
            tecnologia_ram="DDR4",
            capacidad_ram=8,
            tecnologia_disco="SSD",
            capacidad_disco=256,
            num_puertos_usb=3,
            num_puertos_hdmi=1,
            marca_monitor="Dell",
            pulgadas=15.6,
            precio=800.00,
            usuarios_id=1,
            id=101
        )

        self.assertEqual(computador.marca, "Dell")
        self.assertEqual(computador.categoria, "Portátil")
        self.assertEqual(computador.marca_cpu, "Intel")
        self.assertEqual(computador.velocidad_cpu, 2.5)
        self.assertEqual(computador.capacidad_ram, 8)
        self.assertEqual(computador.capacidad_disco, 256)
        self.assertEqual(computador.precio, 800.00)
        self.assertEqual(computador.usuarios_id, 1)
        self.assertEqual(computador.id, 101)
        # Prueba la representación __repr__
        self.assertIn("Dell", repr(computador))
        self.assertIn("Portátil", repr(computador))


class TestComputadorRepository(unittest.TestCase):
    """
    Pruebas unitarias para el ComputadorRepository.
    Simula las interacciones con la base de datos.
    """

    @patch('src.db.session')  # Simula la sesión de la base de datos
    def test_find_all(self, mock_db_session):
        """
        Verifica que find_all llama correctamente a la sesión de la DB y devuelve resultados.
        """
        mock_computador1 = Computador(
            "HP", "Escritorio", "AMD", 3.0, "DDR4", 16, "HDD", 1000, 4, 2, "HP", 24.0, 1200.00, usuarios_id=2
        )
        mock_computador2 = Computador(
            "Lenovo", "Portátil", "Intel", 2.0, "DDR4", 8, "SSD", 512, 2, 1, "Lenovo", 14.0, 950.00, usuarios_id=1
        )
        mock_db_session.execute.return_value.scalars.return_value.all.return_value = [
            mock_computador1,
            mock_computador2,
        ]

        computadores = ComputadorRepository.find_all()
        self.assertEqual(len(computadores), 2)
        self.assertEqual(computadores[0].marca, "HP")
        self.assertEqual(computadores[1].categoria, "Portátil")
        # Asegúrate de que los métodos de SQLAlchemy fueron llamados
        mock_db_session.execute.assert_called_once()

    @patch('src.db.session')
    def test_find_by_id(self, mock_db_session):
        """
        Verifica que find_by_id llama correctamente a db.session.get y devuelve el objeto.
        """
        mock_computador = Computador("Acer", "Gaming", "Intel", 4.0, "DDR5", 32, "SSD", 1024, 5, 3, "Acer", 27.0, 2500.00, usuarios_id=3, id=5)
        mock_db_session.get.return_value = mock_computador

        computador_encontrado = ComputadorRepository.find_by_id(5)
        self.assertIsNotNone(computador_encontrado)
        self.assertEqual(computador_encontrado.id, 5)
        self.assertEqual(computador_encontrado.marca, "Acer")
        mock_db_session.get.assert_called_once_with(Computador, 5)

    @patch('src.db.session')
    def test_save_new_computador(self, mock_db_session):
        """
        Verifica que save agregue y haga commit para un nuevo computador.
        """
        nuevo_computador = Computador("Asus", "Ultrabook", "AMD", 1.8, "LPDDR4", 16, "SSD", 512, 2, 1, "Asus", 13.3, 1100.00, usuarios_id=4)
        
        # Simula que save devuelve el mismo objeto después de guardarlo
        mock_db_session.add.return_value = None
        mock_db_session.commit.return_value = None
        
        resultado = ComputadorRepository.save(nuevo_computador)
        
        mock_db_session.add.assert_called_once_with(nuevo_computador)
        mock_db_session.commit.assert_called_once()
        self.assertEqual(resultado, nuevo_computador) 

    @patch('src.db.session')
    def test_delete_computador(self, mock_db_session):
        """
        Verifica que delete elimina y haga commit para un computador.
        """
        computador_a_eliminar = Computador("Viejo", "Antiguo", "Intel", 1.0, "DDR2", 4, "HDD", 160, 2, 0, "CRT", 17.0, 100.00, usuarios_id=1, id=99)
        
        ComputadorRepository.delete(computador_a_eliminar)
        
        mock_db_session.delete.assert_called_once_with(computador_a_eliminar)
        mock_db_session.commit.assert_called_once()

    @patch('src.db.session')
    def test_find_by_multiple_criteria_containing_ignore_case(self, mock_db_session):
        """
        Verifica que la búsqueda por múltiples criterios funciona con la lógica correcta.
        """
        criterio = "intel"
        mock_computador1 = Computador("Dell", "Portátil", "Intel", 2.5, "DDR4", 8, "SSD", 256, 3, 1, "Dell", 15.6, 800.00, usuarios_id=1)
        mock_computador2 = Computador("HP", "Escritorio", "Intel", 3.5, "DDR4", 16, "HDD", 1000, 4, 2, "HP", 24.0, 1200.00, usuarios_id=2)
        
        mock_db_session.execute.return_value.scalars.return_value.all.return_value = [mock_computador1, mock_computador2]

        resultados = ComputadorRepository.find_by_multiple_criteria_containing_ignore_case(criterio)

        self.assertEqual(len(resultados), 2)
        self.assertIn("Intel", resultados[0].marca_cpu)
        self.assertIn("Intel", resultados[1].marca_cpu)


class TestComputadorService(unittest.TestCase):
    """
    Pruebas unitarias para el ComputadorService.
    Simula las interacciones con el repositorio.
    """

    def setUp(self):
        """
        Configura un mock del repositorio antes de cada prueba.
        """
        self.mock_computador_repository = MagicMock(spec=ComputadorRepository)
        self.computador_service = ComputadorService(self.mock_computador_repository)
        self.dummy_computador = Computador(
            "Dummy", "Test", "Test CPU", 1.0, "DDR", 4, "HDD", 100, 1, 0, "Test Monitor", 10.0, 100.00, usuarios_id=1, id=1
        )

    def test_obtener_computador_por_id(self):
        """
        Verifica que el servicio llama al repositorio para obtener por ID.
        """
        self.mock_computador_repository.find_by_id.return_value = self.dummy_computador
        computador = self.computador_service.obtener_computador_por_id(1)
        self.assertIsNotNone(computador)
        self.assertEqual(computador.id, 1)
        self.mock_computador_repository.find_by_id.assert_called_once_with(1)

    def test_obtener_todos_los_computadores(self):
        """
        Verifica que el servicio llama al repositorio para obtener todos.
        """
        self.mock_computador_repository.find_all.return_value = [self.dummy_computador]
        computadores = self.computador_service.obtener_todos_los_computadores()
        self.assertEqual(len(computadores), 1)
        self.mock_computador_repository.find_all.assert_called_once()

    def test_crear_computador(self):
        """
        Verifica que el servicio llama al repositorio para guardar un nuevo computador.
        """
        self.mock_computador_repository.save.return_value = self.dummy_computador
        computador_creado = self.computador_service.crear_computador(self.dummy_computador)
        self.assertIsNotNone(computador_creado)
        self.mock_computador_repository.save.assert_called_once_with(self.dummy_computador)

    def test_actualizar_computador(self):
        """
        Verifica que el servicio llama al repositorio para actualizar un computador.
        """
        self.mock_computador_repository.save.return_value = self.dummy_computador
        computador_actualizado = self.computador_service.actualizar_computador(self.dummy_computador)
        self.assertIsNotNone(computador_actualizado)
        self.mock_computador_repository.save.assert_called_once_with(self.dummy_computador)

    def test_eliminar_computador_existente(self):
        """
        Verifica que el servicio llama al repositorio para eliminar un computador existente.
        """
        self.mock_computador_repository.find_by_id.return_value = self.dummy_computador
        self.computador_service.eliminar_computador(1)
        self.mock_computador_repository.find_by_id.assert_called_once_with(1)
        self.mock_computador_repository.delete.assert_called_once_with(self.dummy_computador)

    def test_eliminar_computador_no_existente(self):
        """
        Verifica que el servicio no intenta eliminar un computador que no existe.
        """
        self.mock_computador_repository.find_by_id.return_value = None
        with self.assertLogs('root', level='INFO') as cm: 
             self.computador_service.eliminar_computador(999)
             self.assertIn("Advertencia: No se encontró computador con ID 999 para eliminar.", cm.output[0])
        
        self.mock_computador_repository.find_by_id.assert_called_once_with(999)
        self.mock_computador_repository.delete.assert_not_called() 

    def test_buscar_computadores_por_criterio(self):
        """
        Verifica que el servicio llama al repositorio para buscar por criterio.
        """
        self.mock_computador_repository.find_by_multiple_criteria_containing_ignore_case.return_value = [self.dummy_computador]
        resultados = self.computador_service.buscar_computadores_por_criterio("Test")
        self.assertEqual(len(resultados), 1)
        self.mock_computador_repository.find_by_multiple_criteria_containing_ignore_case.assert_called_once_with("Test")


if __name__ == '__main__':
    unittest.main()

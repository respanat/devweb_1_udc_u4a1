from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

from src.models.entities.computador import Computador
from src.models.repositories.computador_repository import ComputadorRepository


class ComputadorService:
    def __init__(self, computador_repository: ComputadorRepository):
        self.computador_repository = computador_repository

    def obtener_computador_por_id(self, id: int) -> Optional[Computador]:
        return self.computador_repository.find_by_id(id)

    def obtener_todos_los_computadores(self) -> List[Computador]:
        return self.computador_repository.find_all()

    def crear_computador(self, computador: Computador) -> Computador:
        return self.computador_repository.save(computador)

    def actualizar_computador(self, computador: Computador) -> Computador:
        return self.computador_repository.save(computador)

    def eliminar_computador(self, id: int):
        computador_a_eliminar = self.computador_repository.find_by_id(id)
        if computador_a_eliminar:
            self.computador_repository.delete(computador_a_eliminar)
        else:
            logger.warning(f"Advertencia: No se encontró computador con ID {id} para eliminar.")

    def buscar_computadores_por_criterio(self, criterio: str) -> List[Computador]:
        return self.computador_repository.find_by_multiple_criteria_containing_ignore_case(criterio)

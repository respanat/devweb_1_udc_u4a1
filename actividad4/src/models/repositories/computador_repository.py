from src import db
from src.models.entities.computador import Computador
from typing import List, Optional
from sqlalchemy import or_


class ComputadorRepository:
    
    @staticmethod
    def find_all() -> List[Computador]:
        return db.session.execute(db.select(Computador)).scalars().all()

    @staticmethod
    def find_by_id(id: int) -> Optional[Computador]:
        return db.session.get(Computador, id)

    @staticmethod
    def save(computador: Computador) -> Computador:
       db.session.add(computador)
       db.session.commit()
       return computador

    @staticmethod
    def delete(computador: Computador):
       db.session.delete(computador)
       db.session.commit()

    @staticmethod
    def find_by_marca_containing_ignore_case(criterio: str) -> List[Computador]:
        return db.session.execute(
            db.select(Computador).filter(Computador.marca.ilike(f'%{criterio}%'))
        ).scalars().all()

    @staticmethod
    def find_by_categoria_containing_ignore_case(criterio: str) -> List[Computador]:
       return db.session.execute(
            db.select(Computador).filter(Computador.categoria.ilike(f'%{criterio}%'))
        ).scalars().all()

    @staticmethod
    def find_by_multiple_criteria_containing_ignore_case(criterio: str) -> List[Computador]:
       search_pattern = f'%{criterio}%' # Patrón para la búsqueda (ej. %valor%)

       return db.session.execute(
            db.select(Computador).filter(
                or_(
                    Computador.marca.ilike(search_pattern),
                    Computador.categoria.ilike(search_pattern),
                    Computador.marca_cpu.ilike(search_pattern),
                    Computador.tecnologia_ram.ilike(search_pattern),
                    Computador.tecnologia_disco.ilike(search_pattern),
                    Computador.marca_monitor.ilike(search_pattern)
                )
            )
        ).scalars().all()

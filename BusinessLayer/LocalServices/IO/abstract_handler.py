from abc import ABC, abstractmethod
from typing import List

from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from BusinessLayer.BusinessObjects.modele import Modele


class AbstractHandler(ABC):
    @abstractmethod
    def import_from_file(self, path, id_superviseur: int, id_lot: int,
                         model: Modele, encoding: str = 'utf-8') -> List[FicheAdresse]:
        raise NotImplementedError

    @abstractmethod
    def export_to_file(self, fiches: List[FicheAdresse], path: str) -> bool:
        raise NotImplementedError

from abc import ABC, abstractmethod
from typing import Optional, Sequence

from pyscreener.docking.data import CalculationData
from pyscreener.docking.metadata import CalculationMetadata

class DockingRunner(ABC):
    @staticmethod
    @abstractmethod
    def prepare_receptor(data: CalculationData) -> CalculationData:
        pass

    @staticmethod
    @abstractmethod
    def prepare_ligand(data: CalculationData) -> CalculationData:
        pass

    @staticmethod
    @abstractmethod
    def run(data: CalculationData) -> Optional[Sequence[float]]:
        pass

    @staticmethod
    @abstractmethod
    def prepare_and_run(data: CalculationData) -> CalculationData:
        pass
    
    @staticmethod
    def validate_metadata(metadata: CalculationMetadata):
        return
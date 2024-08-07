from abc import ABC, abstractmethod

class ExportClient(ABC):
    @abstractmethod
    def export(self, project_id: int, format: str, **kwargs):
        pass
    

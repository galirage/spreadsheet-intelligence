from abc import ABC, abstractmethod


class BaseLoader(ABC):
    """
    Abstract base class for core loader.

    Attributes:
        file_path (str): The path to the file to be loaded.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    @abstractmethod
    def load(self):
        """
        Abstract method to load the file. This method should be implemented by subclasses.
        """
        pass

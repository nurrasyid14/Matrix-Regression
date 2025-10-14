#base_loader.py

import pandas as pd
from abc import ABC, abstractmethod

class BaseLoader(ABC):
    """
    Abstract base class for all dataset loaders.
    """

    def __init__(self, path: str):
        self.path = path
        self.data = None

    @abstractmethod
    def load(self) -> pd.DataFrame:
        """Load the dataset into a pandas DataFrame."""
        pass

    def preview(self, n: int = 5):
        """Preview the first n rows of the dataset."""
        if self.data is None:
            raise ValueError("No dataset loaded yet. Call `.load()` first.")
        return self.data.head(n)

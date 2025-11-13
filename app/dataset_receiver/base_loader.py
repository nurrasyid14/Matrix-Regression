import pandas as pd

class BaseLoader:
    """
    Base class for all dataset loaders.
    Provides a consistent interface and shared logic.
    """

    def __init__(self, path: str):
        self.path = path
        self.data = None

    def load(self) -> pd.DataFrame:
        """Abstract method — must be implemented in subclasses."""
        raise NotImplementedError("Subclasses must implement this method.")

#base_cleaner.py

import pandas as pd
from abc import ABC, abstractmethod

class BaseCleaner(ABC):
    """
    Abstract base class for all preprocessing components.
    """

    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply the transformation and return a cleaned DataFrame."""
        pass

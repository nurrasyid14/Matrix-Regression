#json_loader.py

import pandas as pd
from .base_loader import BaseLoader
from .validator import validate_dataframe

class JSONLoader(BaseLoader):
    """
    Loads JSON datasets into pandas DataFrames.
    """

    def load(self) -> pd.DataFrame:
        self.data = pd.read_json(self.path)
        validate_dataframe(self.data)
        return self.data

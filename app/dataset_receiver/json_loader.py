import pandas as pd
from .base_loader import BaseLoader
from .validator import validate_dataframe

class JSONLoader(BaseLoader):
    """
    Loads JSON datasets into pandas DataFrames.
    """

    def load(self) -> pd.DataFrame:
        # Pandas read_json can handle records, columns, split, etc.
        self.data = pd.read_json(self.path)
        validate_dataframe(self.data)
        return self.data

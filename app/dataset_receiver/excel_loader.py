#excel_loader.py

import pandas as pd
from .base_loader import BaseLoader
from .validator import validate_dataframe

class ExcelLoader(BaseLoader):
    """
    Loads Excel datasets into pandas DataFrames.
    """

    def load(self) -> pd.DataFrame:
        self.data = pd.read_excel(self.path)
        validate_dataframe(self.data)
        return self.data

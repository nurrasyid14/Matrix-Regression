import pandas as pd
from .base_loader import BaseLoader
from .validator import validate_dataframe

class ExcelLoader(BaseLoader):
    """
    Loads Excel datasets (.xls, .xlsx) into pandas DataFrames.
    """

    def load(self) -> pd.DataFrame:
        # Pandas automatically detects sheet if none provided
        self.data = pd.read_excel(self.path)
        validate_dataframe(self.data)
        return self.data

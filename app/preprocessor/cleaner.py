#cleaner.py

import pandas as pd
from .base_cleaner import BaseCleaner

class DataCleaner(BaseCleaner):
    """
    General-purpose data cleaning (whitespace, duplicates, empty values).
    """

    def __init__(self, drop_duplicates=True, drop_empty_rows=True, strip_whitespace=True):
        self.drop_duplicates = drop_duplicates
        self.drop_empty_rows = drop_empty_rows
        self.strip_whitespace = strip_whitespace

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        if self.strip_whitespace:
            df.columns = df.columns.str.strip()
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        if self.drop_duplicates:
            df = df.drop_duplicates()

        if self.drop_empty_rows:
            df = df.dropna(how='all')

        return df

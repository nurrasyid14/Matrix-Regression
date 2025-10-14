#encoder.py

import pandas as pd
from .base_cleaner import BaseCleaner

class DataEncoder(BaseCleaner):
    """
    Encodes categorical columns using one-hot encoding.
    """

    def __init__(self, drop_first=False):
        self.drop_first = drop_first

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = pd.get_dummies(df, drop_first=self.drop_first)
        return df

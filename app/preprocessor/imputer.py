#imputer.py

import pandas as pd
from .base_cleaner import BaseCleaner

class DataImputer(BaseCleaner):
    """
    Fills missing values with mean, median, or mode.
    """

    def __init__(self, strategy='mean'):
        self.strategy = strategy

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for col in df.select_dtypes(include=['float', 'int']).columns:
            if df[col].isnull().any():
                if self.strategy == 'mean':
                    df[col].fillna(df[col].mean(), inplace=True)
                elif self.strategy == 'median':
                    df[col].fillna(df[col].median(), inplace=True)
                elif self.strategy == 'mode':
                    df[col].fillna(df[col].mode().iloc[0], inplace=True)
        return df

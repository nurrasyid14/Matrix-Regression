#scaler.py

import pandas as pd
from .base_cleaner import BaseCleaner

class DataScaler(BaseCleaner):
    """
    Standardizes numeric columns (Z-score normalization).
    """

    def __init__(self, normalize=True):
        self.normalize = normalize
        self.means_ = {}
        self.stds_ = {}

    def fit(self, df: pd.DataFrame):
        numeric_cols = df.select_dtypes(include=['float', 'int']).columns
        self.means_ = df[numeric_cols].mean().to_dict()
        self.stds_ = df[numeric_cols].std().replace(0, 1).to_dict()
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        numeric_cols = df.select_dtypes(include=['float', 'int']).columns
        if self.normalize and self.means_:
            for col in numeric_cols:
                df[col] = (df[col] - self.means_[col]) / self.stds_[col]
        return df

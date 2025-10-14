#outlier_handler.py

import pandas as pd
from .base_cleaner import BaseCleaner

class OutlierHandler(BaseCleaner):
    """
    Detects and caps outliers using IQR method.
    """

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        numeric_cols = df.select_dtypes(include=['float', 'int']).columns

        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            df[col] = df[col].clip(lower, upper)

        return df

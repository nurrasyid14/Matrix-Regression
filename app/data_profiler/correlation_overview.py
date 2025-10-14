#correlation_overview.py

import pandas as pd

class CorrelationOverview:
    """
    Provides correlation matrix for numeric columns.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_correlation_matrix(self) -> pd.DataFrame:
        return self.df.corr(numeric_only=True).round(3)

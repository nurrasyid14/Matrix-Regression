#missing_values.py

import pandas as pd

class MissingValues:
    """
    Calculates missing value counts and percentages.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_missing_summary(self) -> pd.DataFrame:
        missing_count = self.df.isna().sum()
        missing_pct = (missing_count / len(self.df)) * 100
        summary = pd.DataFrame({
            "missing_count": missing_count,
            "missing_percent": missing_pct.round(2)
        })
        return summary

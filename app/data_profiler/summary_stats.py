#summary_stats

import pandas as pd

class SummaryStats:
    """
    Generates descriptive statistics for numeric columns.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def describe(self) -> pd.DataFrame:
        """Return basic descriptive statistics."""
        return self.df.describe().T

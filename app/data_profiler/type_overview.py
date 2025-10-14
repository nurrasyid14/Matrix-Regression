#type_overview.py

import pandas as pd

class TypeOverview:
    """
    Provides an overview of column data types.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_overview(self) -> pd.DataFrame:
        type_counts = self.df.dtypes.value_counts()
        detail = pd.DataFrame({
            "column": self.df.columns,
            "dtype": self.df.dtypes.astype(str)
        })
        return {
            "type_counts": type_counts.to_dict(),
            "column_details": detail
        }

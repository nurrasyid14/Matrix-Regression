import pandas as pd

def validate_dataframe(df: pd.DataFrame):
    """
    Ensure DataFrame is not empty and has valid structure.
    """
    if df is None or df.empty:
        raise ValueError("Loaded dataset is empty.")
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Loaded data must be a pandas DataFrame.")

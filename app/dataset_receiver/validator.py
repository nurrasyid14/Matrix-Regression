#validator.py

import pandas as pd

def validate_dataframe(df: pd.DataFrame):
    """
    Perform basic validation checks on a DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Loaded object is not a pandas DataFrame.")
    if df.empty:
        raise ValueError("Loaded dataset is empty.")
    if df.isnull().all().all():
        raise ValueError("Dataset contains only NaN values.")
    return True

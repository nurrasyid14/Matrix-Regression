#profiler.py

import pandas as pd
from .summary_stats import SummaryStats
from .missing_values import MissingValues
from .type_overview import TypeOverview
from .correlation_overview import CorrelationOverview


class DataProfiler:
    """
    Central class for generating data summaries and insights.
    Works on numeric-only datasets (ideally from DatasetGate).
    """

    def __init__(self, df: pd.DataFrame):
        if not isinstance(df, pd.DataFrame):
            raise TypeError("DataProfiler requires a pandas DataFrame.")
        self.df = df.select_dtypes(include=["number"])  # safety guard

        self.summary = SummaryStats(self.df)
        self.missing = MissingValues(self.df)
        self.types = TypeOverview(self.df)
        self.correlation = CorrelationOverview(self.df)

    def profile(self):
        """
        Return a comprehensive profile as a dictionary.
        """
        return {
            "shape": self.df.shape,
            "types": self.types.get_overview(),
            "missing": self.missing.get_missing_summary(),
            "summary_stats": self.summary.describe(),
            "correlation": self.correlation.get_correlation_matrix(),
        }

    def to_json(self) -> str:
        """Return the profile report as a JSON string."""
        import json
        return json.dumps(self.profile(), indent=2, default=str)

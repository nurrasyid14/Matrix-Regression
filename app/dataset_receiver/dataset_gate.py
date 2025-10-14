import os
import pandas as pd
from datetime import datetime
from .csv_loader import CSVLoader
from .excel_loader import ExcelLoader
from .json_loader import JSONLoader
from .utils import check_file_exists
from .validator import validate_dataframe


class DatasetGate:
    """
    Smart dataset receiver that automatically detects file type
    (CSV, Excel, JSON) and loads it into a pandas DataFrame.

    Features:
      - Auto file-type detection
      - Auto conversion of numeric-like strings
      - Numeric-only filtering
      - Logging of discarded columns
    """

    SUPPORTED_EXTENSIONS = {
        ".csv": CSVLoader,
        ".xlsx": ExcelLoader,
        ".xls": ExcelLoader,
        ".json": JSONLoader,
    }

    def __init__(self, path: str, numeric_only: bool = True, log_path: str = "dataset_gate.log"):
        self.path = path
        self.numeric_only = numeric_only
        self.log_path = log_path
        self.loader = None
        self.data = None

    def _detect_loader(self):
        """Detect correct loader class based on file extension."""
        _, ext = os.path.splitext(self.path)
        ext = ext.lower()
        if ext not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type '{ext}'. Supported types: {', '.join(self.SUPPORTED_EXTENSIONS.keys())}"
            )
        return self.SUPPORTED_EXTENSIONS[ext]

    def _auto_convert_numeric(self, df: pd.DataFrame) -> pd.DataFrame:
        """Attempt to convert numeric-looking string columns to numeric dtype."""
        for col in df.columns:
            if df[col].dtype == "object":
                converted = pd.to_numeric(df[col], errors="ignore")
                if not converted.equals(df[col]):
                    df[col] = converted
        return df

    def _filter_numeric(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filter to numeric columns only and log discarded ones."""
        all_columns = set(df.columns)
        numeric_df = df.select_dtypes(include=["number"])
        numeric_columns = set(numeric_df.columns)
        discarded = list(all_columns - numeric_columns)

        if discarded:
            self._log_discarded(discarded)

        if numeric_df.empty:
            raise ValueError(
                "Dataset contains no numeric columns. Non-numeric data is not accepted."
            )

        return numeric_df

    def _log_discarded(self, discarded_cols):
        """Log discarded columns to a file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] Discarded non-numeric columns: {', '.join(discarded_cols)}\n")

    def receive(self) -> pd.DataFrame:
        """
        Main entry point:
          1. Check file existence
          2. Detect loader
          3. Load dataset
          4. Validate DataFrame
          5. Auto-convert numeric strings
          6. Filter numeric columns (optional)
        """
        check_file_exists(self.path)
        loader_class = self._detect_loader()
        self.loader = loader_class(self.path)
        df = self.loader.load()
        validate_dataframe(df)

        # Convert numeric-like strings
        df = self._auto_convert_numeric(df)

        # Keep numeric columns only
        if self.numeric_only:
            df = self._filter_numeric(df)

        self.data = df
        return self.data

    def preview(self, n: int = 5) -> pd.DataFrame:
        """Preview first n rows of the loaded dataset."""
        if self.data is None:
            raise ValueError("No dataset loaded yet. Call `.receive()` first.")
        return self.data.head(n)

    @staticmethod
    def quick_load(file_path: str, numeric_only: bool = True) -> pd.DataFrame:
        """
        Convenience method to load dataset without explicitly creating a DatasetGate instance.
        """
        gate = DatasetGate(file_path, numeric_only=numeric_only)
        return gate.receive()

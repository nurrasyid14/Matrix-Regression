#__init__.py 

# --- Dataset Receiver ---
from app.dataset_receiver import (
    dataset_gate,
    csv_loader,
    excel_loader,
    json_loader,
    validator,
    utils,
)

# --- Preprocessor ---
from app.preprocessor import (
    base_cleaner,
    cleaner,
    encoder,
    imputer,
    outlier_handler,
    scaler,
)

# --- Matrix Operations ---
from app.matrice_ops import arithmatics, linalg

# --- Data Profiler ---
from app.data_profiler import (
    profiler,
    summary_stats,
    correlation_overview,
    missing_values,
    type_overview,
)

# --- Regressor ---
from app.regressor import (
    linear_regression,
    metrics,
    model_base,
    preprocessing,
)

# --- Visualizations ---
from app.visualizations import (
    base_plotter,
    scatter_plot,
    box_plot,
    histogram,
    correlation_heatmap,
    pair_plot,
    utils as viz_utils,
)

__all__ = [
    # Dataset Receiver
    "dataset_gate",
    "csv_loader",
    "excel_loader",
    "json_loader",
    "validator",
    "utils",
    # Preprocessor
    "base_cleaner",
    "cleaner",
    "encoder",
    "imputer",
    "outlier_handler",
    "scaler",
    # Matrix Operations
    "arithmatics",
    "linalg",
    # Data Profiler
    "profiler",
    "summary_stats",
    "correlation_overview",
    "missing_values",
    "type_overview",
    # Regressor
    "linear_regression",
    "metrics",
    "model_base",
    "preprocessing",
    # Visualizations
    "base_plotter",
    "scatter_plot",
    "box_plot",
    "histogram",
    "correlation_heatmap",
    "pair_plot",
    "viz_utils",
]

# Optional: version tracking for releases
__version__ = "0.1.0"

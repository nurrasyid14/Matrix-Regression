"""
main.py
=========
Application runner for RegressorMatrice.

This file orchestrates:
1. Dataset ingestion
2. Data preprocessing
3. Matrix operations
4. Regression model training
5. Visualization of results
"""

import sys
from pathlib import Path

# Add app to path for relative imports
sys.path.append(str(Path(__file__).resolve().parent / "app"))

# --- Import pipeline components ---
from dataset_receiver.dataset_gate import DatasetGate
from preprocessor.cleaner import DataCleaner
from regressor.linear_regression import LinearRegressor
from visualizations.scatter_plot import ScatterPlot
from visualizations.correlation_heatmap import CorrelationHeatmap


def main():
    print("🔹 Starting RegressorMatrice Pipeline...")

    # -----------------------------
    # 1️⃣ Dataset Loading
    # -----------------------------
    gate = DatasetGate()
    df = gate.load_dataset("data/sample_dataset.csv")  # replace with your dataset path

    print(f"✅ Dataset Loaded: {df.shape[0]} rows, {df.shape[1]} columns")

    # -----------------------------
    # 2️⃣ Preprocessing
    # -----------------------------
    cleaner = DataCleaner(df)
    df_clean = cleaner.clean()

    print("✅ Data cleaned and ready for processing.")

    # -----------------------------
    # 3️⃣ Regression Model Training
    # -----------------------------
    regressor = LinearRegressor(df_clean)
    regressor.train(target="y")  # specify your target column

    print("✅ Model training complete.")

    # -----------------------------
    # 4️⃣ Visualization
    # -----------------------------
    scatter = ScatterPlot(df_clean, x_col="x1", y_col="y")
    scatter.show()

    heatmap = CorrelationHeatmap(df_clean)
    heatmap.show()

    print("✅ Visualization complete.")

    # -----------------------------
    # 5️⃣ Evaluation / Summary
    # -----------------------------
    results = regressor.evaluate()
    print("\n📊 Regression Summary:")
    for k, v in results.items():
        print(f"  {k}: {v:.4f}")

    print("\n🎉 RegressorMatrice Run Completed Successfully!")


if __name__ == "__main__":
    main()

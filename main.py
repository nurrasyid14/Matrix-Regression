"""
main.py
=========
Interactive runner for RegressorMatrice.

This version lets the USER provide their own dataset path
instead of hardcoding it.
"""

import sys
from pathlib import Path

# Add app modules to path
sys.path.append(str(Path(__file__).resolve().parent / "app"))

# Import core modules
from app.dataset_receiver.dataset_gate import DatasetGate
from app.preprocessor.cleaner import DataCleaner
from app.regressor.linear_regression import LinearRegressor
from app.visualizations.scatter_plot import ScatterPlot
from app.visualizations.correlation_heatmap import CorrelationHeatmap


def main():
    print("\n🔹 Welcome to RegressorMatrice!")
    print("This app will perform data cleaning, regression, and visualization.\n")

    # -----------------------------
    # 1️⃣ Ask user for dataset path
    # -----------------------------
    dataset_path = input("📂 Please enter the path to your dataset file: ").strip()

    if not Path(dataset_path).exists():
        print(f"❌ Error: File not found at '{dataset_path}'")
        return

    # -----------------------------
    # 2️⃣ Load dataset
    # -----------------------------
    gate = DatasetGate()
    df = gate.load_dataset(dataset_path)
    print(f"✅ Dataset Loaded: {df.shape[0]} rows × {df.shape[1]} columns")

    # -----------------------------
    # 3️⃣ Preprocessing
    # -----------------------------
    cleaner = DataCleaner(df)
    df_clean = cleaner.clean()
    print("✅ Data cleaned successfully.")

    # -----------------------------
    # 4️⃣ Target column input
    # -----------------------------
    print("\nAvailable columns:")
    print(", ".join(df_clean.columns))
    target_col = input("\n🎯 Enter the target column for regression: ").strip()

    if target_col not in df_clean.columns:
        print(f"❌ Error: '{target_col}' not found in dataset columns.")
        return

    # -----------------------------
    # 5️⃣ Regression
    # -----------------------------
    regressor = LinearRegressor(df_clean)
    regressor.train(target=target_col)
    print("✅ Model training complete.")

    # -----------------------------
    # 6️⃣ Visualizations
    # -----------------------------
    try:
        # Choose example feature for plotting
        features = [c for c in df_clean.columns if c != target_col]
        if features:
            x_feature = features[0]
            scatter = ScatterPlot(df_clean, x_col=x_feature, y_col=target_col)
            scatter.show()

        heatmap = CorrelationHeatmap(df_clean)
        heatmap.show()

        print("✅ Visualization complete.")
    except Exception as e:
        print(f"⚠️ Visualization skipped due to: {e}")

    # -----------------------------
    # 7️⃣ Evaluation Summary
    # -----------------------------
    results = regressor.evaluate()
    print("\n📊 Regression Summary:")
    for k, v in results.items():
        print(f"  {k}: {v:.4f}")

    print("\n🎉 RegressorMatrice completed successfully!")


if __name__ == "__main__":
    main()

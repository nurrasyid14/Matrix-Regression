# app/main.py

import os
import pandas as pd
from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from flask_session import Session
from werkzeug.utils import secure_filename
from sklearn.model_selection import train_test_split

# Custom imports (pastikan module ini ada di app/)
from dataset_receiver.dataset_gate import DatasetGate
from regressor import (
    LinearRegression,
    RidgeRegression,
    PolynomialRegression,
    r2_score,
    mean_squared_error,
)

# -------------------------------------
# Flask Configuration
# -------------------------------------
app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)

CORS(app, supports_credentials=True)

UPLOAD_FOLDER = "uploads_temp"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Flask session configuration
app.config.update(
    UPLOAD_FOLDER=UPLOAD_FOLDER,
    SECRET_KEY="super-secure-key",
    SESSION_TYPE="filesystem",
)

# Enable server-side sessions
Session(app)

# -------------------------------------
# Routes
# -------------------------------------
@app.route("/")
def index():
    """Serve main web interface"""
    return render_template("index.html")


# -------------------------------------
# Upload Dataset
# -------------------------------------
@app.route("/api/upload", methods=["POST"])
def upload_dataset():
    """Upload and cache dataset to user session"""
    if "file" not in request.files:
        return jsonify({"error": "No file key named 'file' found."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename provided."}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Load dataset, hanya numeric columns
        df = DatasetGate.quick_load(filepath, numeric_only=True)
        os.remove(filepath)

        # Simpan dataset di session
        session["dataset_json"] = df.to_json(orient="split")
        session.modified = True

        # Preview untuk frontend
        preview_html = df.head(5).to_html(classes="table table-sm", index=False)

        return jsonify({
            "message": "Dataset uploaded successfully.",
            "columns": df.columns.tolist(),
            "preview": preview_html
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500


# -------------------------------------
# Run Regression Analysis
# -------------------------------------
@app.route("/api/analyze", methods=["POST"])
def run_regression_api():
    """Execute regression and return metrics, coefficients, and charts"""
    if "dataset_json" not in session:
        return jsonify({"error": "No dataset found in session. Upload first."}), 400

    try:
        df = pd.read_json(session["dataset_json"], orient="split")

        data = request.get_json()
        features = data.get("features")
        target = data.get("target")
        model_type = data.get("modelType", "linear")
        degree = int(data.get("degree", 2))
        alpha = float(data.get("alpha", 1.0))

        if not features or not target:
            return jsonify({"error": "Missing features or target."}), 400

        X = df[features].to_numpy()
        y = df[target].to_numpy()

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Pilih model
        if model_type == "ridge":
            model = RidgeRegression(alpha=alpha)
        elif model_type == "polynomial":
            model = PolynomialRegression(degree=degree)
        else:
            model = LinearRegression()

        # Fit model dan prediksi
        model.fit(X_train, y_train)
        predictions = model.predict(X_test).ravel()

        # Hitung metrics
        r2 = r2_score(y_test, predictions)
        mse = mean_squared_error(y_test, predictions)
        rmse = mse ** 0.5

        metrics_summary = {
            "R²": round(r2, 4),
            "MSE": round(mse, 4),
            "RMSE": round(rmse, 4),
            "Samples Used": int(len(X)),
        }

        # Koefisien
        coeffs = getattr(model, "coefficients", getattr(model, "coef_", []))
        coeffs = coeffs.ravel().tolist() if hasattr(coeffs, "ravel") else list(coeffs)
        intercept = coeffs[0] if len(coeffs) > 0 else 0.0
        feature_coeffs = coeffs[1:] if len(coeffs) > 1 else []

        # Persamaan regresi
        equation = (
            f"{target} = {intercept:.4f} + "
            + " + ".join([f"({coef:.4f} * {feat})" for coef, feat in zip(feature_coeffs, features)])
            if feature_coeffs else f"{target} = {intercept:.4f}"
        )

        # Chart koefisien
        feature_chart = {
            "labels": features,
            "datasets": [{
                "label": "Feature Influence",
                "data": feature_coeffs,
                "backgroundColor": "rgba(54, 162, 235, 0.6)"
            }]
        }

        # Chart Actual vs Predicted
        scatter_chart = {
            "points": [{"x": float(a), "y": float(p)} for a, p in zip(y_test.tolist(), predictions.tolist())],
            "line": [
                {"x": float(min(y_test)), "y": float(min(y_test))},
                {"x": float(max(y_test)), "y": float(max(y_test))}
            ]
        }

        return jsonify({
            "modelType": model_type,
            "equation": equation,
            "metrics": metrics_summary,
            "featureChartData": feature_chart,
            "accuracyChartData": scatter_chart,
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500


# -------------------------------------
# Entry Point
# -------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

# app/main.py

import os
import pandas as pd
from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
from sklearn.model_selection import train_test_split

# Custom imports
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

app.config.update(
    UPLOAD_FOLDER=UPLOAD_FOLDER,
    SECRET_KEY="super-secure-key",
    SESSION_TYPE="filesystem",
)

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
@app.route("/api/run-regression", methods=["POST"])
def run_regression():
    """Execute regression and return metrics, coefficients, and charts"""
    if "dataset_json" not in session:
        return jsonify({"error": "No dataset found in session. Upload first."}), 400

    try:
        df = pd.read_json(session["dataset_json"], orient="split")
        data = request.get_json()

        features = data.get("features")
        target = data.get("target")
        model_type = data.get("modelType", "linear")

        if not features or not target:
            return jsonify({"error": "Missing features or target."}), 400

        X = df[features]
        y = df[target]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Select model
        if model_type == "ridge":
            model = RidgeRegression(alpha=float(data.get("alpha", 1.0)))
        elif model_type == "polynomial":
            model = PolynomialRegression(degree=int(data.get("degree", 2)))
        else:
            model = LinearRegression()

        model.fit(X_train.to_numpy(), y_train.to_numpy())
        predictions = model.predict(X_test.to_numpy())

        # Compute metrics
        r2 = r2_score(y_test, predictions)
        mse = mean_squared_error(y_test, predictions)
        rmse = mse ** 0.5

        metrics_summary = {
            "R²": round(r2, 4),
            "MSE": round(mse, 4),
            "RMSE": round(rmse, 4),
            "MAE": 0.0,
            "Explained Variance": round(r2, 4)
        }

        # Coefficients
        coeffs = getattr(model, "coefficients", getattr(model, "coef_", []))
        intercept = coeffs[0] if len(coeffs) else 0
        feature_coeffs = coeffs[1:] if len(coeffs) > 1 else []

        equation = f"{target} = {intercept:.4f}"
        if feature_coeffs is not None:
            equation += " + " + " + ".join(
                [f"({c:.4f} * {f})" for c, f in zip(feature_coeffs, features)]
            )

        # Chart data
        feature_chart = {
            "labels": features,
            "datasets": [{
                "label": "Feature Influence",
                "data": [float(c) for c in feature_coeffs],
                "backgroundColor": "rgba(54, 162, 235, 0.6)"
            }]
        }

        scatter_chart = {
            "points": [
                {"x": float(a), "y": float(p)}
                for a, p in zip(y_test.tolist(), predictions.flatten().tolist())
            ],
            "line": [
                {"x": min(y_test), "y": min(y_test)},
                {"x": max(y_test), "y": max(y_test)},
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
# Run Regression Analysis
# -------------------------------------
@app.route("/api/run-regression", methods=["POST"])
def run_regression():
    """Execute regression and return metrics, coefficients, and charts"""
    if "dataset_json" not in session:
        return jsonify({"error": "No dataset found in session. Upload first."}), 400

    try:
        df = pd.read_json(session["dataset_json"], orient="split")

        data = request.get_json()
        features = data.get("features")
        target = data.get("target")
        model_type = data.get("modelType", "linear")

        if not features or not target:
            return jsonify({"error": "Missing features or target."}), 400

        X = df[features]
        y = df[target]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Select model
        if model_type == "ridge":
            model = RidgeRegression(alpha=1.0)
        elif model_type == "polynomial":
            model = PolynomialRegression(degree=2)
        else:
            model = LinearRegression()

        # Fit and predict
        model.fit(X_train.to_numpy(), y_train.to_numpy())
        predictions = model.predict(X_test.to_numpy())

        # Compute metrics
        r2 = r2_score(y_test, predictions)
        mse = mean_squared_error(y_test, predictions)

        # Prepare coefficients & equation
        coeffs = (
            model.coefficients
            if hasattr(model, "coefficients")
            else getattr(model, "coef_", [])
        )

        if len(coeffs) > 1:
            intercept = coeffs[0]
            feature_coeffs = coeffs[1:]
            equation = f"{target} = {intercept:.4f} + " + " + ".join(
                [f"({coef:.4f} * {feat})" for coef, feat in zip(feature_coeffs, features)]
            )
        else:
            equation = "Model coefficients unavailable."

        # Chart data for dashboard
        feature_chart = {
            "labels": features,
            "datasets": [{
                "label": "Feature Influence",
                "data": feature_coeffs.tolist(),
                "backgroundColor": "rgba(54, 162, 235, 0.6)"
            }]
        }

        scatter_chart = {
            "points": [
                {"x": float(a), "y": float(p)}
                for a, p in zip(y_test.tolist(), predictions.flatten().tolist())
            ]
        }

        # Dashboard metrics cards
        metrics_summary = [
            {"name": "R² Score", "value": round(r2, 4)},
            {"name": "Mean Squared Error", "value": round(mse, 4)},
            {"name": "Samples Used", "value": len(X)},
        ]

        return jsonify({
            "modelType": model_type,
            "equation": equation,
            "metrics": metrics_summary,
            "featureChart": feature_chart,
            "scatterChart": scatter_chart,
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

# app/main.py
import os
from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS 
from werkzeug.utils import secure_filename
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

# Import your modules (assumes PYTHONPATH or working dir includes /app)
from dataset_receiver.dataset_gate import DatasetGate
from regressor.linear_regression import LinearRegression

# --- Flask app config ---
app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
CORS(app)

UPLOAD_FOLDER = "uploads_temp"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Make sure to set a real secret key in production
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'dev-secret-key-for-local')

# In-memory store for uploaded DataFrames keyed by filename (or session id)
# NOTE: this is ephemeral (lost on restart); fine for dev.
datasets = {}


# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/upload", methods=["POST"])
def upload_dataset():
    """
    Accept file upload (key: 'dataset'), use DatasetGate to load numeric-only DataFrame,
    save the DataFrame in the server-side `datasets` dict, and store the filename in session.
    Response: { "columns": [...column names...] }
    """
    if "dataset" not in request.files:
        return jsonify({"error": "No file part named 'dataset' in request."}), 400

    file = request.files["dataset"]
    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Use DatasetGate to load and filter numeric columns
        # We use quick_load convenience (returns DataFrame with numeric-only columns)
        df = DatasetGate.quick_load(filepath, numeric_only=True)

        # store dataframe server-side (in-memory) and keep filename in session
        datasets[filename] = df
        session['uploaded_filename'] = filename

        # remove temp file (we keep DataFrame in memory)
        try:
            os.remove(filepath)
        except Exception:
            pass

        return jsonify({"columns": df.columns.tolist()})

    except Exception as e:
        # For debugging, include the error message in response
        return jsonify({"error": f"Failed to process file on backend: {str(e)}"}), 500


@app.route("/api/run-regression", methods=["POST"])
def run_regression():
    """
    Run regression using the dataset uploaded earlier (filename in session).
    Expect JSON payload: { "features": [...], "target": "y" }
    Returns JSON with equation, coefficients for chart, and accuracy chart data.
    """
    filename = session.get('uploaded_filename')
    if not filename:
        return jsonify({"error": "No uploaded dataset found in session. Please upload a file first."}), 400

    df = datasets.get(filename)
    if df is None:
        return jsonify({"error": "Uploaded dataset not found on server. Please re-upload."}), 400

    payload = request.get_json() or {}
    features = payload.get("features")
    target = payload.get("target")

    if not features or not target:
        return jsonify({"error": "Missing 'features' or 'target' in request body."}), 400

    # Validate columns exist
    missing = [c for c in features + [target] if c not in df.columns]
    if missing:
        return jsonify({"error": f"Columns not found in dataset: {missing}"}), 400

    try:
        # Prepare data (use numpy arrays for the matrix regressors)
        X = df[features].to_numpy(dtype=float)
        y = df[target].to_numpy(dtype=float)

        # Split for a quick test set to visualize prediction performance
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Instantiate your matrix-based LinearRegression (note: no normalize arg)
        model = LinearRegression(fit_intercept=True)
        model.fit(X_train, y_train)

        # Predictions
        y_pred = model.predict(X_test)  # returns 1D array

        # Build equation string
        # model.coefficients is expected to be 1D array: [intercept, coef1, coef2, ...]
        coeffs = getattr(model, "coefficients", None)
        if coeffs is None:
            # fallback: try attribute name used in other versions
            coeffs = getattr(model, "coef_", None)

        if coeffs is None:
            # If still None, return error
            return jsonify({"error": "Model coefficients not available after fitting."}), 500

        coeffs = np.asarray(coeffs).flatten()
        intercept = float(coeffs[0])
        feature_coeffs = coeffs[1:].tolist()

        equation = f"{target} = {intercept:.4f}"
        for feat, c in zip(features, feature_coeffs):
            equation += f" + ({c:.4f} * {feat})"

        # Prepare feature chart data (bar chart)
        feature_chart_data = {
            "labels": features,
            "datasets": [{
                "label": "Koefisien",
                "data": feature_coeffs,
                # keep color info simple; your UI may override
                "backgroundColor": "rgba(153, 102, 255, 0.6)"
            }]
        }

        # Prepare accuracy chart data (actual vs predicted scatter + identity line)
        y_test_list = list(map(float, y_test.tolist()))
        predictions_list = list(map(float, y_pred.tolist()))

        min_val = min(min(y_test_list), min(predictions_list))
        max_val = max(max(y_test_list), max(predictions_list))

        accuracy_chart_data = {
            "points": [{"x": a, "y": p} for a, p in zip(y_test_list, predictions_list)],
            "line": [{"x": min_val, "y": min_val}, {"x": max_val, "y": max_val}]
        }

        return jsonify({
            "equation": equation,
            "featureChartData": feature_chart_data,
            "accuracyChartData": accuracy_chart_data
        })

    except Exception as e:
        # Print stacktrace server-side to help debugging
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500


# simple health endpoint
@app.route("/health", methods=["GET"])
def health():
    return "OK", 200


if __name__ == "__main__":
    # production should disable debug and use WSGI server
    app.run(host="0.0.0.0", port=5000, debug=True)

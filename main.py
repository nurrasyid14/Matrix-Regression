from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
from app.dataset_receiver.dataset_gate import DatasetGate
from app.regressor.linear_regression import LinearRegression

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Store uploaded dataset temporarily in memory
datasets = {}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    """
    Upload dataset, validate numeric columns, and return list of columns.
    """
    if "dataset" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["dataset"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Load and validate dataset
    try:
        gate = DatasetGate(file_path)
        df = gate.receive()
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # Save dataset in memory with a temporary key
    datasets["current"] = df

    # Return numeric columns to JS
    return jsonify({"columns": df.columns.tolist()})


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Run regression with selected X/Y columns and return results.
    """
    data = request.json
    x_cols = data.get("x_columns", [])
    y_col = data.get("y_column")

    df = datasets.get("current")
    if df is None:
        return jsonify({"error": "No dataset uploaded"}), 400

    if not x_cols or not y_col:
        return jsonify({"error": "Select X and Y columns"}), 400

    # Run Linear Regression
    X = df[x_cols]
    y = df[y_col]
    model = LinearRegressor(df)
    model.fit(X, y)
    coefficients = dict(zip(x_cols, model.coef_))
    intercept = model.intercept_
    predictions = model.predict(X).tolist()

    # Prepare JSON for frontend (equation, coefficients, predictions)
    regression_eq = f"{y_col} = {intercept:.4f} + " + " + ".join([f"{coef:.4f}*{col}" for col, coef in coefficients.items()])
    result = {
        "equation": regression_eq,
        "coefficients": coefficients,
        "predictions": predictions
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

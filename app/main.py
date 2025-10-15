# main.py
from flask import Flask, request, jsonify
import os
import pandas as pd
from dataset_receiver.dataset_gate import DatasetGate
from regressor.linear_regression import LinearRegression

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store uploaded datasets in memory (optional)
datasets = {}

@app.route("/api/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save file temporarily
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Use DatasetGate to validate & filter numeric columns
    try:
        gate = DatasetGate(filepath)
        df = gate.receive()
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # Store dataframe in memory
    datasets[file.filename] = df

    return jsonify({"message": "File uploaded", "columns": df.columns.tolist()})

@app.route("/api/run_analysis", methods=["POST"])
def run_analysis():
    data = request.json
    filename = data.get("filename")
    features = data.get("features")  # list of feature column names
    target = data.get("target")      # target column name

    if not filename or filename not in datasets:
        return jsonify({"error": "Dataset not found"}), 400
    if not features or not target:
        return jsonify({"error": "Features or target not provided"}), 400

    df = datasets[filename]
    X = df[features]
    y = df[target]

    # Run linear regression
    try:
        model = LinearRegressor()
        model.fit(X, y)
        predictions = model.predict(X)
        coef_dict = dict(zip(features, model.coef_))
        equation = f"{target} = " + " + ".join([f"{coef:.4f}*{col}" for col, coef in coef_dict.items()])
        results = {
            "equation": equation,
            "coefficients": coef_dict,
            "actual": y.tolist(),
            "predicted": predictions.tolist()
        }
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(results)

@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

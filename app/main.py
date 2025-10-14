from flask import Flask, request, jsonify, send_from_directory
import os
from app.dataset_receiver.dataset_gate import DatasetGate
from app.regressor.linear_regression import LinearRegression 
from app.visualizations.base_plotter import BasePlotter 

app = Flask(__name__, static_folder="frontend/static", template_folder="frontend/templates")

# Route to serve the main page
@app.route("/")
def index():
    return send_from_directory(app.template_folder, "index.html")

# Upload dataset
@app.route("/upload", methods=["POST"])
def upload_dataset():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    file_path = os.path.join("/tmp", file.filename)
    file.save(file_path)

    try:
        gate = DatasetGate(file_path)
        df = gate.receive()
        columns = df.columns.tolist()
        return jsonify({"columns": columns})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Run regression
@app.route("/run-analysis", methods=["POST"])
def run_analysis():
    data = request.json
    features = data.get("features")
    target = data.get("target")
    file_path = data.get("file_path")

    try:
        gate = DatasetGate(file_path)
        df = gate.receive()

        model = LinearRegressionModel()
        model.fit(df[features], df[target])
        results = model.summary()

        # Optional: generate plots
        plots = Plotter(df, model).generate_all()

        return jsonify({"results": results, "plots": plots})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

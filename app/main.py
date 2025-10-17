import os
import pandas as pd
from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
from sklearn.model_selection import train_test_split

# Custom modules
from dataset_receiver.dataset_gate import DatasetGate
from regressor import (
    LinearRegression,
    RidgeRegression,
    PolynomialRegression,
    r2_score,
    mean_squared_error,
)

# -------------------------------
# Flask Configuration
# -------------------------------
app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
CORS(app, supports_credentials=True)

UPLOAD_FOLDER = "uploads_temp"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config.update(
    UPLOAD_FOLDER=UPLOAD_FOLDER,
    SECRET_KEY='super-secure-key',
    SESSION_TYPE='filesystem'  # Keeps session working across Docker/Nginx
)

# -------------------------------
# Routes
# -------------------------------

@app.route("/")
def index():
    return render_template("index.html")

# -------------------------------
# Upload Dataset
# -------------------------------
@app.route("/api/upload", methods=["POST"])
def upload_dataset():
    if "dataset" not in request.files:
        return jsonify({"error": "No file key named 'dataset' found."}), 400

    file = request.files["dataset"]
    if file.filename == "":
        return jsonify({"error": "Empty filename provided."}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Load dataset using DatasetGate
        df = DatasetGate.quick_load(filepath, numeric_only=True)
        os.remove(filepath)

        # Store dataset in session
        session['dataset_json'] = df.to_json(orient='split')
        session.modified = True

        return jsonify({"message": "Dataset uploaded successfully.", "columns": df.columns.tolist()})

    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

# -------------------------------
# Run Regression Analysis
# -------------------------------
@app.route("/api/run-regression", methods=["POST"])
def run_regression():
    if 'dataset_json' not in session:
        return jsonify({"error": "No dataset found in session. Upload first."}), 400

    try:
        df = pd.read_json(session['dataset_json'], orient='split')

        data = request.get_json()
        features = data.get("features")
        target = data.get("target")
        model_type = data.get("modelType", "linear")  # linear, ridge, polynomial

        if not features or not target:
            return jsonify({"error": "Missing features or target."}), 400

        X = df[features]
        y = df[target]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Select model type
        if model_type == "ridge":
            model = RidgeRegression(alpha=1.0)
        elif model_type == "polynomial":
            model = PolynomialRegression(degree=2)
        else:
            model = LinearRegression()

        model.fit(X_train.to_numpy(), y_train.to_numpy())
        predictions = model.predict(X_test.to_numpy())

        # Compute metrics
        r2 = r2_score(y_test, predictions)
        mse = mean_squared_error(y_test, predictions)

        coeffs = model.coefficients if hasattr(model, "coefficients") else []
        equation = (
            f"{target} = {coeffs[0]:.4f} + "
            + " + ".join([f"({c:.4f} * {f})" for c, f in zip(coeffs[1:], features)])
            if len(coeffs) > 1
            else "Model coefficients not available"
        )

        response = {
            "modelType": model_type,
            "equation": equation,
            "metrics": {
                "r2_score": round(r2, 4),
                "mean_squared_error": round(mse, 4)
            },
            "coefficients": dict(zip(["Intercept"] + features, coeffs)),
        }

        return jsonify(response)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

# -------------------------------
# Run App
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

import os
import pandas as pd
from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
from sklearn.model_selection import train_test_split

# Import internal modules
from dataset_receiver.dataset_gate import DatasetGate
from regressor.linear_regression import LinearRegression
from regressor.polynomial_regression import PolynomialRegression
from regressor.ridge_regression import RidgeRegression
from regressor.metrics import (
    r2_score,
    mean_squared_error,
    root_mean_squared_error,
    mean_absolute_error,
    explained_variance_score
)

# --- Flask App Configuration ---
app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
CORS(app)

UPLOAD_FOLDER = "uploads_temp"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'super-secret-key-change-this'  # Change later in production

# --- ROUTES ---

@app.route("/")
def index():
    """Serve the main web page."""
    return render_template("index.html")


@app.route("/api/upload", methods=["POST"])
def upload_dataset():
    """Handle dataset upload and store it temporarily in session."""
    if "dataset" not in request.files:
        return jsonify({"error": "No file uploaded under key 'dataset'"}), 400

    file = request.files["dataset"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        df = DatasetGate.quick_load(filepath, numeric_only=True)
        session['dataset_json'] = df.to_json(orient='split')
        os.remove(filepath)

        return jsonify({"columns": df.columns.tolist()})
    except Exception as e:
        return jsonify({"error": f"Failed to process file: {str(e)}"}), 500


@app.route("/api/run-regression", methods=["POST"])
def run_regression_analysis():
    """Run selected regression model and return metrics + plots."""
    if 'dataset_json' not in session:
        return jsonify({"error": "No dataset found in session. Upload first."}), 400

    try:
        df = pd.read_json(session['dataset_json'], orient='split')
        config = request.json

        features = config.get("features")
        target = config.get("target")
        model_type = config.get("modelType", "linear")
        degree = config.get("degree", 2)
        alpha = config.get("alpha", 1.0)

        if not features or not target:
            return jsonify({"error": "Features or target missing in request"}), 400

        X = df[features].values
        y = df[target].values

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Select model
        if model_type == "linear":
            model = LinearRegression(fit_intercept=True)
        elif model_type == "polynomial":
            model = PolynomialRegression(degree=degree)
        elif model_type == "ridge":
            model = RidgeRegression(alpha=alpha)
        else:
            return jsonify({"error": f"Unknown model type: {model_type}"}), 400

        # Train + Predict
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        # Compute metrics
        metrics = {
            "R²": round(r2_score(y_test, predictions), 4),
            "MSE": round(mean_squared_error(y_test, predictions), 4),
            "RMSE": round(root_mean_squared_error(y_test, predictions), 4),
            "MAE": round(mean_absolute_error(y_test, predictions), 4),
            "Explained Variance": round(explained_variance_score(y_test, predictions), 4)
        }

        # Equation / Coeff summary
        coef_str = model.summary()

        # Feature impact chart
        if hasattr(model, "coefficients"):
            coeffs = model.coefficients
            feature_chart_data = {
                'labels': features,
                'datasets': [{
                    'label': 'Coefficients',
                    'data': coeffs[1:].tolist() if model.fit_intercept else coeffs.tolist(),
                    'backgroundColor': 'rgba(153, 102, 255, 0.6)'
                }]
            }
        else:
            feature_chart_data = {}

        # Accuracy chart (scatter)
        y_test_list = y_test.tolist()
        predictions_list = predictions.flatten().tolist()
        min_val = min(min(y_test_list), min(predictions_list))
        max_val = max(max(y_test_list), max(predictions_list))
        accuracy_chart_data = {
            'points': [{'x': actual, 'y': pred} for actual, pred in zip(y_test_list, predictions_list)],
            'line': [{'x': min_val, 'y': min_val}, {'x': max_val, 'y': max_val}]
        }

        # Response
        return jsonify({
            "modelType": model_type,
            "summary": coef_str,
            "metrics": metrics,
            "featureChartData": feature_chart_data,
            "accuracyChartData": accuracy_chart_data
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Regression failed: {str(e)}"}), 500


# --- Main Entry Point ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

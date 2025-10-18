# Matrix-Regression App

A comprehensive web application for matrix operations and regression analysis built with Python and Flask, containerized with Docker.

## 🚀 Features

### 1. Dataset Receiver

* Load datasets from CSV, XLSX, or JSON files.
* Generate random datasets for testing.
* Dataset statistics and preview visualization.
* Automatic preprocessing: numeric column selection.

### 2. Basic Matrix Operations

* Matrix addition, subtraction, multiplication, division.
* Element-wise operations.
* Real-time computation and validation.

### 3. Linear Algebra Operations

* Transpose, inverse, determinant of matrices.
* Identity matrix generation.
* Advanced matrix operations.

### 4. Regression Machine

* Linear Regression.
* Polynomial Regression.
* Ridge Regression (L2 regularization).
* Model evaluation metrics: R², MSE, RMSE, MAE, Explained Variance.
* Prediction capabilities.

### 5. Web Interface

* Interactive, Flask-based frontend.
* Dataset preview and feature/target selection.
* Dynamic charts for coefficients and prediction accuracy.
* Real-time status messages and analysis feedback.

### 6. Frontend Usage & Interaction

#### Upload Dataset

* Click **“Choose file”** to select a CSV, XLSX, or JSON file.
* Only numeric columns are used.
* First 5 rows are displayed as a **preview table**.

#### Select Features & Target

* **Features (X):** Check one or more columns as input variables.
* **Target (Y):** Select one column as output variable.
* Quick selection via **“Select All”** or **“Deselect All”**.

#### Choose Regression Type

* **Linear Regression** – standard linear model.
* **Ridge Regression** – L2-regularized linear regression; configure α.
* **Polynomial Regression** – expands features to polynomial degree.

#### Run Analysis

* Click **“Run Analysis”**.
* Status messages show progress.
* Results displayed:

  * **Equation:** Fitted regression formula.
  * **Metrics:** R², MSE, RMSE, MAE, Explained Variance.
  * **Feature Coefficients:** Bar chart for feature influence.
  * **Actual vs Predicted:** Scatter plot with 45° reference line.

#### Reset

* Click **“Reset”** to clear selections, charts, and metrics.

#### Charts

* **Feature Coefficients:** Bar chart visualizing feature weights.
* **Accuracy Chart:** Scatter plot comparing actual vs predicted values.
* Interactive and responsive.

💡 **Tip:** For best performance, keep datasets under 50,000 rows × 200 features.

---

## 📁 Project Structure

```
Matrix-Regression/
├── README.md
├── [app]
│   ├── [data_profiler]
│   │   ├── __init__.py
│   │   ├── correlation_overview.py
│   │   ├── missing_values.py
│   │   ├── profiler.py
│   │   ├── summary_stats.py
│   │   └── type_overview.py
│   ├── [dataset_receiver]
│   │   ├── [uploads]
│   │   │   └── (EMPTY DIRECTORY)
│   │   ├── __init__.py
│   │   ├── base_loader.py
│   │   ├── csv_loader.py
│   │   ├── dataset_gate.py
│   │   ├── excel_loader.py
│   │   ├── json_loader.py
│   │   ├── utils.py
│   │   └── validator.py
│   ├── [matrice_ops]
│   │   ├── [arithmatics]
│   │   │   ├── __init__.py
│   │   │   ├── addition.py
│   │   │   ├── exponential.py
│   │   │   ├── fraction.py
│   │   │   ├── multiplication.py
│   │   │   └── subtraction.py
│   │   ├── [linalg]
│   │   │   ├── __init__.py
│   │   │   ├── determinant.py
│   │   │   ├── inverse.py
│   │   │   ├── rank.py
│   │   │   └── transpose.py
│   │   └── __init__.py
│   ├── [preprocessor]
│   │   ├── __init__.py
│   │   ├── base_cleaner.py
│   │   ├── cleaner.py
│   │   ├── encoder.py
│   │   ├── imputer.py
│   │   ├── outlier_handler.py
│   │   └── scaler.py
│   ├── [regressor]
│   │   ├── __init__.py
│   │   ├── linear_regression.py
│   │   ├── metrics.py
│   │   ├── model_base.py
│   │   ├── polynomial_regression.py
│   │   ├── preprocessing.py
│   │   └── ridge_regression.py
│   ├── [visualizations]
│   │   ├── __init__.py
│   │   ├── base_plotter.py
│   │   ├── box_plot.py
│   │   ├── correlation_heatmap.py
│   │   ├── histogram.py
│   │   ├── pair_plot.py
│   │   ├── scatter_plot.py
│   │   └── utils.py
│   ├── [frontend]
│   │   ├── [static]
│   │   │   ├── [assets]
│   │   │   │   └── loading.txt
│   │   │   ├── [css]
│   │   │   │   └── style.css
│   │   │   └── [js]
│   │   │       ├── api.js
│   │   │       ├── main.js
│   │   │       └── ui.js
│   │   └── [templates]
│   │       └── index.html
│   ├── __init__.py
│   └── main.py
└──[docker]
    ├── .dockerignore
    ├── docker-compose.yml
    ├── dockerfile
    ├── entrypoint.sh
    ├── nginx.conf
    └── requirements.txt
```
---

## 🐳 Docker Setup

### Prerequisites

* Docker
* Docker Compose

### Quick Start

```bash
# Clone and run
git clone <repository-url>
cd Matrix-Regression

# Build and start with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Manual Docker Build

```bash
# Build the image
docker build -t matrix-regression .

# Run the container
docker run -p 5000:5000 matrix-regression
```

---

## 🧮 Algorithm Complexity Analysis

### Matrix Operations

| Operation             | Time Complexity | Space Complexity | Method                  |
| --------------------- | --------------- | ---------------- | ----------------------- |
| Addition/Subtraction  | O(m×n)          | O(m×n)           | Element-wise            |
| Element-wise Multiply | O(m×n)          | O(m×n)           | Hadamard product        |
| Matrix Multiplication | O(m×n×p)        | O(m×p)           | Naive algorithm         |
| Transpose             | O(m×n)          | O(m×n)           | Element swapping        |
| Determinant           | O(n³)           | O(n²)            | LU decomposition        |
| Inverse               | O(n³)           | O(n²)            | Gaussian elimination    |
| Identity Matrix       | O(n²)           | O(n²)            | Diagonal initialization |

### Regression Algorithms

| Algorithm             | Training Time        | Prediction Time | Method                      |
| --------------------- | -------------------- | --------------- | --------------------------- |
| Linear Regression     | O(n²×p + p³)         | O(p)            | Normal equation             |
| Polynomial Regression | O((n×d)²×p + (p×d)³) | O(p×d)          | Feature expansion           |
| Ridge Regression      | O(n²×p + p³)         | O(p)            | Regularized normal equation |

**Notation:**

* **n** = number of samples
* **p** = number of features
* **d** = polynomial degree
* **m×n** = matrix dimensions

---

## 📊 Performance Specifications

* **Max Dataset Size:** 50,000 rows × 200 features
* **Matrix Operations:** Optimized with NumPy BLAS
* **Memory Usage:** Efficient up to 2GB datasets
* **Response Time:** < 5 seconds for standard operations
* **Container Resources:** 2GB RAM, 2+ CPU cores recommended

---

## 🔧 Development

```bash
# Development with Docker
docker-compose -f docker-compose.yml up --build

# Run tests
docker-compose exec app pytest

# Code quality
docker-compose exec app black app/
docker-compose exec app flake8 app/
```

---

## 🚀 Production Deployment

```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d

# Scale application
docker-compose up -d --scale app=3

# Monitor containers
docker-compose ps
docker-compose logs -f
```

---

## 🔒 Environment Variables

```bash
FLASK_ENV=production
FLASK_DEBUG=0
DATABASE_URL=sqlite:///data/app.db
UPLOAD_FOLDER=/app/data/uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
```

---

## 📈 Monitoring & Logs

```bash
# View logs
docker-compose logs -f app

# Check container usage
docker stats

# Health check
curl http://localhost:5000/health
```

---

## 🗂️ Data Persistence

* Data persisted in `./data` volume
* Uploads stored in `./data/uploads`
* Database in `./data/app.db`

---

## 🐛 Troubleshooting

```bash
# Check container status
docker-compose ps

# Restart services
docker-compose restart

# Rebuild from scratch
docker-compose down -v
docker-compose up --build
```

---

## 📄 License

MIT License - see LICENSE file for details.

# Matrix-Regression App

A comprehensive web application for matrix operations and regression analysis built with Python and Flask, containerized with Docker.

## 🚀 Features

### 1. Dataset Receiver
- Load datasets from CSV/JSON files
- Generate random datasets for testing
- Dataset statistics and visualization
- Data preprocessing capabilities

### 2. Basic Operations
- Matrix addition, subtraction, multiplication, division
- Element-wise operations
- Real-time computation
- Result validation

### 3. Linear Algebra Operations
- Matrix transpose, inverse, determinant
- Identity matrix generation
- Matrix multiplication
- Advanced linear algebra functions

### 4. Regression Machine
- Linear Regression
- Polynomial Regression  
- Ridge Regression
- Model evaluation metrics (R², MSE, RMSE)
- Prediction capabilities

### 5. Web Interface
- Flask-based frontend
- Interactive Plotly visualizations
- Real-time results display
- RESTful API endpoints

## 📁 Project Structure

```
Matrix-Regression/
├── README.md
├── app
│   ├── __init__.py
│   ├── data_profiler
│   │   ├── __init__.py
│   │   ├── correlation_overview.py
│   │   ├── missing_values.py
│   │   ├── profiler.py
│   │   ├── summary_stats.py
│   │   └── type_overview.py
│   ├── dataset_receiver
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-311.pyc
│   │   │   ├── base_loader.cpython-311.pyc
│   │   │   ├── csv_loader.cpython-311.pyc
│   │   │   ├── dataset_gate.cpython-311.pyc
│   │   │   ├── excel_loader.cpython-311.pyc
│   │   │   ├── json_loader.cpython-311.pyc
│   │   │   ├── utils.cpython-311.pyc
│   │   │   └── validator.cpython-311.pyc
│   │   ├── base_loader.py
│   │   ├── csv_loader.py
│   │   ├── dataset_gate.py
│   │   ├── excel_loader.py
│   │   ├── json_loader.py
│   │   ├── utils.py
│   │   └── validator.py
│   ├── frontend
│   │   ├── static
│   │   │   ├── assets
│   │   │   │   └── loading.txt
│   │   │   ├── css
│   │   │   │   └── style.css
│   │   │   └── js
│   │   │       ├── api.js
│   │   │       ├── main.js
│   │   │       └── ui.js
│   │   └── templates
│   │       └── index.html
│   ├── main.py
│   ├── matrice_ops
│   │   ├── __init__.py
│   │   ├── arithmatics
│   │   │   ├── __init__.py
│   │   │   ├── addition.py
│   │   │   ├── exponential.py
│   │   │   ├── fraction.py
│   │   │   ├── multiplication.py
│   │   │   └── subtraction.py
│   │   └── linalg
│   │       ├── __init__.py
│   │       ├── determinant.py
│   │       ├── inverse.py
│   │       ├── rank.py
│   │       └── transpose.py
│   ├── preprocessor
│   │   ├── __init__.py
│   │   ├── base_cleaner.py
│   │   ├── cleaner.py
│   │   ├── encoder.py
│   │   ├── imputer.py
│   │   ├── outlier_handler.py
│   │   └── scaler.py
│   ├── regressor
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-311.pyc
│   │   │   ├── linear_regression.cpython-311.pyc
│   │   │   ├── metrics.cpython-311.pyc
│   │   │   ├── model_base.cpython-311.pyc
│   │   │   └── preprocessing.cpython-311.pyc
│   │   ├── linear_regression.py
│   │   ├── metrics.py
│   │   ├── model_base.py
│   │   └── preprocessing.py
│   └── visualizations
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── __init__.cpython-311.pyc
│       │   ├── base_plotter.cpython-311.pyc
│       │   ├── box_plot.cpython-311.pyc
│       │   ├── correlation_heatmap.cpython-311.pyc
│       │   ├── histogram.cpython-311.pyc
│       │   ├── pair_plot.cpython-311.pyc
│       │   ├── scatter_plot.cpython-311.pyc
│       │   └── utils.cpython-311.pyc
│       ├── base_plotter.py
│       ├── box_plot.py
│       ├── correlation_heatmap.py
│       ├── histogram.py
│       ├── pair_plot.py
│       ├── scatter_plot.py
│       └── utils.py
└── docker
    ├── docker-compose.yml
    ├── dockerfile
    ├── entrypoint.sh
    ├── nginx.conf
    └── requirements.txt

20 directories, 81 files
```

## 🐳 Docker Setup

### Prerequisites
- Docker
- Docker Compose

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

## 🛠️ Development with Docker

```bash
# Development mode with hot reload
docker-compose -f docker-compose.dev.yml up

# Run tests in container
docker-compose exec app pytest tests/

# Access container shell
docker-compose exec app bash

# View application logs
docker-compose logs app
```

## 📦 Docker Configuration Files

### docker-compose.yml

### docker/Dockerfile


## 🧮 Algorithm Complexity Analysis

### Matrix Operations
| Operation | Time Complexity | Space Complexity | Method |
|-----------|----------------|------------------|--------|
| Addition/Subtraction | O(m×n) | O(m×n) | Element-wise |
| Element-wise Multiply | O(m×n) | O(m×n) | Hadamard product |
| Matrix Multiplication | O(m×n×p) | O(m×p) | Naive algorithm |
| Transpose | O(m×n) | O(m×n) | Element swapping |
| Determinant | O(n³) | O(n²) | LU decomposition |
| Inverse | O(n³) | O(n²) | Gaussian elimination |
| Identity Matrix | O(n²) | O(n²) | Diagonal initialization |

### Regression Algorithms
| Algorithm | Training Time | Prediction Time | Method |
|-----------|---------------|-----------------|--------|
| Linear Regression | O(n²×p + p³) | O(p) | Normal equation |
| Polynomial Regression | O((n×d)²×p + (p×d)³) | O(p×d) | Feature expansion |
| Ridge Regression | O(n²×p + p³) | O(p) | Regularized normal equation |

**Notation:**
- **n** = number of samples
- **p** = number of features  
- **d** = polynomial degree
- **m×n** = matrix dimensions

## 📊 Performance Specifications

- **Maximum Dataset Size**: 50,000 samples × 200 features
- **Matrix Operations**: Optimized using NumPy BLAS
- **Memory Usage**: Efficient handling up to 2GB datasets
- **Response Time**: < 5 seconds for standard operations
- **Container Memory**: 2GB recommended
- **Container CPU**: 2+ cores recommended

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

## 🔒 Environment Variables

```bash
# Application settings
FLASK_ENV=production
FLASK_DEBUG=0
DATABASE_URL=sqlite:///data/app.db
UPLOAD_FOLDER=/app/data/uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
```

## 📈 Monitoring & Logs

```bash
# View real-time logs
docker-compose logs -f app

# Check container resource usage
docker stats

# Access application metrics
curl http://localhost:5000/health
```

## 🗂️ Data Persistence

- Data is persisted in `./data` volume
- Uploads stored in `./data/uploads`
- Database in `./data/app.db`

## 🐛 Troubleshooting

```bash
# Check container status
docker-compose ps

# View detailed logs
docker-compose logs app

# Restart services
docker-compose restart

# Rebuild from scratch
docker-compose down -v
docker-compose up --build
```

## 📄 License

MIT License - see LICENSE file for details.

---

**Docker Benefits:**
- Consistent development and production environments
- Easy deployment and scaling
- Isolated dependencies
- Simplified CI/CD pipeline

Visit `http://localhost:5000` to access the application after starting with Docker Compose.

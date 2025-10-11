# Matrix-Regression App

A comprehensive web application for matrix operations and regression analysis built with Python and Flask.

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

## 📁 Updated Project Structure

```
Matrix-Regression/
├── app/
│   ├── __init__.py
│   ├── dataset_receiver/
│   │   ├── __init__.py
│   │   └── receiver.py
│   ├── operations/
│   │   ├── __init__.py
│   │   └── basic_ops.py
│   ├── linalg/
│   │   ├── __init__.py
│   │   └── linalg_ops.py
│   ├── regressor/
│   │   ├── __init__.py
│   │   └── regression.py
│   └── frontend/
│       ├── __init__.py
│       ├── app.py
│       └── templates/
│           ├── base.html
│           ├── index.html
│           ├── dataset.html
│           ├── basic_ops.html
│           ├── linalg_ops.html
│           └── regression.html
├── requirements.txt
├── main.py
└── run.py
```

## 🛠️ Installation

```bash
# Clone the repository
git clone <repository-url>
cd Matrix-Regression

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

Visit `http://localhost:5000` to access the application.

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

## 🔧 Development

```bash
# Run in development mode
python run.py --debug

# Run tests
pytest tests/

# Code formatting
black app/

# Linting
flake8 app/
```

## 🚀 Deployment

```bash
# Production deployment
gunicorn -w 4 -b 0.0.0.0:5000 app.frontend.app:app
```

## 📈 Future Enhancements

- [ ] Support for larger datasets with chunk processing
- [ ] Additional regression algorithms (Lasso, ElasticNet)
- [ ] Classification models
- [ ] Real-time collaboration features
- [ ] Docker containerization

## 🐛 Bug Reports

Please report bugs and feature requests via GitHub issues.

## 📄 License

MIT License - see LICENSE file for details.

---

**Note**: This application is designed for educational and research purposes. Performance may vary based on hardware specifications and dataset characteristics.

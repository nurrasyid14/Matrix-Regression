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
├── docker/
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
├── requirements.txt
├── main.py
└── run.py
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
```yaml
version: '3.8'

services:
  app:
    build: 
      context: .
      dockerfile: docker/Dockerfile
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - PYTHONUNBUFFERED=1
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./docker/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - app
```

### docker/Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY main.py run.py ./

# Create data directory
RUN mkdir -p /app/data

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "run.py"]
```

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

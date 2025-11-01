# MLOps Project: Plant Classification (Dandelion vs Grass)

🌼 **Binary Image Classification with Full MLOps Pipeline**

## 📋 Project Overview

This project implements a complete MLOps pipeline for classifying plant images (dandelions vs grass) using deep learning. It demonstrates industry best practices including:

- ✅ Data extraction & preprocessing
- ✅ CNN model training with TensorFlow/Keras
- ✅ Experiment tracking with MLflow
- ✅ Model storage in S3 (Minio)
- ✅ REST API with FastAPI
- ✅ React frontend WebApp
- ✅ Docker containerization
- ✅ Docker Compose orchestration
- 🔄 CI/CD with GitHub Actions (optional)
- 🔄 Airflow pipelines (optional)
- 📊 Monitoring (optional)

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Frontend  │────▶│   FastAPI    │────▶│    Model    │
│  (React)    │     │   (8000)     │     │   (.keras)  │
└─────────────┘     └──────────────┘     └─────────────┘
                            │                     │
                            ▼                     ▼
                    ┌──────────────┐     ┌─────────────┐
                    │   MLflow     │     │   Minio S3  │
                    │   (5000)     │     │   (9000)    │
                    └──────────────┘     └─────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- 4GB+ RAM
- 5GB+ disk space

### 1️⃣ Setup Python Environment

```bash
# Clone the repository
cd ML-Ops-project

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Download & Prepare Data

```bash
# Download images from GitHub and clean them
python run_import_clean.py

# This will:
# - Download 200 dandelion + 200 grass images
# - Clean and resize to 256x256
# - Save to cleaned_images_for_model/
```

### 3️⃣ Train Model with MLflow

```bash
# Start MLflow server (in separate terminal)
mlflow server --host 0.0.0.0 --port 5000

# Train the model
python train_with_mlflow.py

# Output:
# - dandelion_grass_cnn.keras (trained model)
# - training_history.png (accuracy/loss plots)
# - MLflow experiment logs
```

Visit **http://localhost:5000** to view MLflow UI with experiment tracking.

### 4️⃣ Run with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Services will be available at:
# - Frontend:  http://localhost:3000
# - API:       http://localhost:8000
# - API Docs:  http://localhost:8000/docs
# - MLflow:    http://localhost:5000
# - Minio:     http://localhost:9001 (admin/minioadmin123)
```

### 5️⃣ Test the API

```bash
# Health check
curl http://localhost:8000/health

# Test prediction with an image
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/image.jpg"

# Or visit http://localhost:8000/docs for Swagger UI
```

## 📁 Project Structure

```
ML-Ops-project/
├── api/
│   └── main.py                    # FastAPI application
├── Front/                         # React frontend
│   ├── src/
│   ├── Dockerfile
│   └── nginx.conf
├── cleaned_images_for_model/      # Processed training data
├── image_data_from_repo/          # Raw downloaded images
├── mlruns/                        # MLflow experiments
├── run_import_clean.py            # Data download script
├── run_train_model.py             # Basic training script
├── train_with_mlflow.py           # Training with MLflow
├── docker-compose.yml             # Services orchestration
├── Dockerfile.api                 # API container
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🎯 Model Details

- **Architecture**: CNN (3 Conv blocks + Dense layers)
- **Input**: 256x256 RGB images
- **Output**: Binary classification (sigmoid)
- **Training**: 15 epochs, batch size 32
- **Split**: 80% train, 20% validation
- **Framework**: TensorFlow/Keras 2.16.1

### Model Performance

- **Validation Accuracy**: 85%
- **Training Accuracy**: 92.4%
- **Training Time**: ~13 minutes (CPU)
- **Model Size**: 170MB

## 🎨 WebApp Features

The React frontend provides:
- ✨ Drag & drop image upload
- 🎯 Real-time prediction with confidence scores
- 📊 Animated progress bars
- 📱 Responsive design (mobile & desktop)
- 🔄 Reclassification support
- ❌ Graceful error handling with fallback

**Tech Stack**: React 18 + TypeScript + Vite + TailwindCSS + Framer Motion

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/predict` | POST | Image classification |
| `/model-info` | GET | Model details |
| `/docs` | GET | Swagger documentation |

## 🐳 Docker Images

### Build Individual Images

```bash
# API
docker build -t your-dockerhub-username/mlops-api:latest -f Dockerfile.api .

# Frontend
docker build -t your-dockerhub-username/mlops-frontend:latest ./Front

# Push to DockerHub
docker push your-dockerhub-username/mlops-api:latest
docker push your-dockerhub-username/mlops-frontend:latest
```

## 🔬 Development Workflow

### Local Development

```bash
# Run API locally
cd api
uvicorn main:app --reload --port 8000

# Run frontend locally
cd Front
npm install
npm run dev
```

### Testing

```bash
# Unit tests (TODO)
pytest tests/

# Integration tests (TODO)
pytest tests/integration/

# Load testing with Locust (TODO)
locust -f tests/load_test.py
```

## 📊 Monitoring & Logging

- **MLflow**: Track experiments, metrics, parameters
- **FastAPI logs**: Request/response logging
- **Docker logs**: `docker-compose logs -f api`

## 🔄 CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
# TODO: Add GitHub Actions workflow for:
# - Automated testing
# - Docker image building
# - Deployment to Kubernetes
```

## ☸️ Kubernetes Deployment (Optional)

```bash
# TODO: Helm charts for:
# - API deployment
# - Frontend deployment
# - MLflow server
# - Minio storage
```

## 🎓 Learning Objectives Achieved

1. ✅ **Data Pipeline**: Automated download, cleaning, preprocessing
2. ✅ **Model Training**: CNN with TensorFlow/Keras (85% accuracy)
3. ✅ **Experiment Tracking**: MLflow integration with metrics logging
4. ✅ **Model Storage**: S3-compatible storage (Minio)
5. ✅ **API Development**: FastAPI with async support + Swagger docs
6. ✅ **Frontend WebApp**: React + TypeScript with real-time predictions
7. ✅ **Containerization**: Docker & Docker Compose orchestration
8. 🔄 **Orchestration**: Airflow DAGs (to be implemented)
9. 🔄 **CI/CD**: GitHub Actions (to be implemented)
10. 🔄 **Monitoring**: Prometheus/Grafana (to be implemented)

## 📝 TODO / Future Improvements

- [ ] Add Airflow DAGs for automated retraining
- [ ] Implement GitHub Actions CI/CD
- [ ] Add Prometheus + Grafana monitoring
- [ ] Deploy to Kubernetes
- [ ] Add unit & integration tests
- [ ] Implement feature store
- [ ] Add load testing with Locust
- [ ] Continuous training (CT) pipeline

## 👥 Team

- [Add team member names]

## 📧 Contact

For questions: prillard.martin@gmail.com

## 📄 License

MIT License

---

**Built with ❤️ for MLOps learning**
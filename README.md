# 🌿 Dandelion vs Grass Classifier - MLOps Project

> Image classification system using Deep Learning and MLOps best practices

Binary classification of dandelion and grass images with MLflow experiment tracking, Model Registry, and containerized deployment.

[![Docker](https://img.shields.io/badge/Docker-Compose-blue)](https://www.docker.com/)
[![MLflow](https://img.shields.io/badge/MLflow-Tracking-orange)](https://mlflow.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-green)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB)](https://reactjs.org/)

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Architecture](#-architecture)
- [Technologies Used](#-technologies-used)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [MLOps Features](#-mlops-features)
- [API Documentation](#-api-documentation)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Project Overview

This project implements a complete MLOps solution for plant image classification (dandelion vs grass) featuring:

- **🧠 CNN Model** trained on TensorFlow/Keras
- **📊 MLflow** for experiment tracking and Model Registry
- **🚀 FastAPI** for prediction API
- **⚛️ React** for user interface
- **🐳 Docker** for containerization
- **📦 MinIO** for S3-compatible storage
- **🔄 Auto-registration** of models on startup

### Features

✅ Real-time image classification with confidence scores
✅ Automatic experiment tracking with MLflow
✅ Model Registry with versioning
✅ Documented REST API (Swagger)
✅ Modern and responsive web interface
✅ S3-compatible artifact storage (MinIO)
✅ Microservices architecture

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User                                │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React)                         │
│                  http://localhost:3001                      │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ↓ POST /predict
┌─────────────────────────────────────────────────────────────┐
│                   API (FastAPI)                             │
│                  http://localhost:8000                      │
│   - Load model from MLflow                                  │
│   - Image preprocessing                                     │
│   - CNN prediction                                          │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ↓
┌─────────────────────────────────────────────────────────────┐
│              MLflow Tracking Server                         │
│                http://localhost:5000                        │
│   - Model Registry                                          │
│   - Experiment tracking                                     │
│   - Artifact storage (→ MinIO)                              │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                 MinIO (S3-compatible)                       │
│           http://localhost:9000 (API)                       │
│           http://localhost:9001 (Console)                   │
│   - Model artifacts storage                                 │
│   - Training history plots                                  │
│   - Metrics and parameters                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technologies Used

### Backend & ML

- **Python 3.11** - Main language
- **TensorFlow/Keras** - Deep Learning framework
- **FastAPI** - Modern, fast API framework
- **MLflow** - Experiment tracking and Model Registry
- **scikit-learn** - ML preprocessing and utilities

### Frontend

- **React 18** - UI framework
- **TypeScript** - Static typing
- **Vite** - Modern build tool
- **Tailwind CSS** - Utility-first styling

### Infrastructure

- **Docker & Docker Compose** - Containerization
- **MinIO** - S3-compatible storage
- **Nginx** - Reverse proxy for frontend
- **Uvicorn** - ASGI server for FastAPI

### MLOps Tools

- **MLflow Model Registry** - Model versioning
- **Auto-registration** - Automatic registration on startup
- **Health checks** - Service monitoring
- **Volume persistence** - Persistent data

---

## 🚀 Installation

### Prerequisites

- **Docker Desktop** ([Download](https://www.docker.com/products/docker-desktop))
- **8 GB RAM** minimum
- **10 GB** free disk space

### Installation in 3 steps

#### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ML-Ops-project.git
cd ML-Ops-project
```

#### 2. Start all services

```bash
docker-compose up --build
```

⏳ **Wait 20-30 seconds** for all services to start...

#### 3. Access the services

Open in your browser:

| Service | URL | Description |
|---------|-----|-------------|
| 🌐 **Frontend** | http://localhost:3001 | User interface |
| 🔮 **API Swagger** | http://localhost:8000/docs | Interactive API documentation |
| 📊 **MLflow UI** | http://localhost:5000 | Tracking & Model Registry |
| 📦 **MinIO Console** | http://localhost:9001 | S3 Storage (minioadmin/minioadmin123) |

**✨ You're ready!**

---

## 💻 Usage

### Via Web Interface

1. Open http://localhost:3001
2. Upload an image of a dandelion or grass
3. Click "Classify"
4. Get the prediction with confidence level

### Via API

#### Health Check

```bash
curl http://localhost:8000/health
```

#### Prediction

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/image.jpg"
```

**Response**:

```json
{
  "predicted_class": "dandelion",
  "confidence": 0.87,
  "probabilities": {
    "dandelion": 0.87,
    "grass": 0.13
  },
  "timestamp": "2025-11-10T10:00:00.123456"
}
```

### Via Python

```python
import requests

# Prediction
with open("image.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/predict",
        files={"file": f}
    )

result = response.json()
print(f"Class: {result['predicted_class']}")
print(f"Confidence: {result['confidence']:.2%}")
```

---

## 📁 Project Structure

```
ML-Ops-project/
├── api/                          # FastAPI API
│   └── main.py                   # Endpoints and API logic
├── Front/                        # React Frontend
│   ├── src/
│   │   ├── App.tsx              # Main application
│   │   └── components/          # React components
│   ├── Dockerfile               # Frontend build
│   └── nginx.conf               # Nginx configuration
├── models/                       # Trained models
│   └── dandelion_grass_cnn.keras
├── scripts/                      # Utility scripts
│   ├── train_with_mlflow.py    # Training with tracking
│   ├── auto_register_model.py  # MLflow auto-registration
│   └── docker_entrypoint.sh    # Startup script
├── data/                         # Training data
│   └── images/                  # Dandelion and grass images
├── docker-compose.yml           # Service orchestration
├── Dockerfile.api              # API Docker image
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🎓 MLOps Features

### 1. Experiment Tracking (MLflow)

Each training run is automatically tracked:

```python
# scripts/train_with_mlflow.py
with mlflow.start_run():
    mlflow.log_param("epochs", 15)
    mlflow.log_param("batch_size", 32)
    mlflow.log_metric("accuracy", 0.95)
    mlflow.keras.log_model(model, "model")
```

**Visualization**: http://localhost:5000

### 2. Model Registry

Models are registered with versioning:

```python
mlflow.register_model(
    model_uri="runs:/RUN_ID/model",
    name="dandelion-grass-classifier"
)
```

**Available stages**:
- `None`: New model
- `Staging`: Under testing
- `Production`: Deployed
- `Archived`: Old model

### 3. Auto-registration

On Docker startup, the model is automatically registered in MLflow Model Registry.

```bash
# Check in logs
docker logs mlops_api | grep "Model registered"
```

### 4. Artifact Storage (MinIO)

All artifacts are stored in MinIO (S3-compatible):
- Models (.keras)
- Metrics (CSV)
- Plots (PNG)
- Metadata (JSON)

**Access**: http://localhost:9001 (minioadmin / minioadmin123)

### 5. Model Versioning

```python
# Load a specific version
model = mlflow.keras.load_model("models:/dandelion-grass-classifier/1")

# Load the Production version
model = mlflow.keras.load_model("models:/dandelion-grass-classifier/Production")
```

---

## 📖 API Documentation

### Endpoints

#### `GET /`

API home page

**Response**:
```json
{
  "message": "Plant Classification API",
  "status": "running",
  "version": "1.0.0"
}
```

#### `GET /health`

API health check

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2025-11-10T10:00:00"
}
```

#### `POST /predict`

Image classification

**Parameters**:
- `file`: Image (JPG, PNG)

**Response**:
```json
{
  "predicted_class": "grass",
  "confidence": 0.92,
  "probabilities": {
    "dandelion": 0.08,
    "grass": 0.92
  },
  "timestamp": "2025-11-10T10:00:00"
}
```

#### `GET /model-info`

Model information

**Response**:
```json
{
  "model_type": "CNN",
  "input_shape": [null, 256, 256, 3],
  "output_shape": [null, 1],
  "classes": ["dandelion", "grass"],
  "total_params": 14839105
}
```

### Interactive Documentation

**Swagger UI**: http://localhost:8000/docs

---

## 🐛 Troubleshooting

### Docker won't start

```bash
# Windows: Open Docker Desktop
# Linux:
sudo systemctl start docker
```

### Port already in use

```bash
# See which process uses the port
netstat -ano | findstr :3001

# Change port in docker-compose.yml
ports:
  - "3002:80"  # Use 3002 instead of 3001
```

### Model won't load

```bash
# Check logs
docker logs mlops_api

# Verify file exists
ls -la models/dandelion_grass_cnn.keras

# Restart API
docker-compose restart api
```

### Services won't start

```bash
# Check container status
docker-compose ps

# View service logs
docker logs mlops_mlflow
docker logs mlops_api

# Restart everything
docker-compose down
docker-compose up -d
```

### "Out of memory" error

Docker Desktop → Settings → Resources → Memory: **Increase to 8 GB**

---

## 🛑 Stop the Project

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (data)
docker-compose down -v
```

---

## 🔧 Development

### Train a new model

```bash
cd scripts
python train_with_mlflow.py
```

The model will be automatically:
- ✅ Trained on the data
- ✅ Tracked in MLflow
- ✅ Saved to MinIO
- ✅ Registered in Model Registry

### Promote a model to Production

```bash
python scripts/promote_model_to_production.py
```

Or via MLflow UI:
1. http://localhost:5000/#/models
2. Click on your model
3. Select the version
4. Stage → **Production**

### Restart the API

```bash
docker-compose restart api
```

The API will automatically load the new version from MLflow!

---

## 📊 Monitoring

### Check services

```bash
docker-compose ps
```

### View logs in real-time

```bash
docker logs -f mlops_api
docker logs -f mlops_mlflow
```

### Check metrics

MLflow UI → http://localhost:5000 → Experiments

---

## 🚀 Deployment

### On a server (VPS)

1. **Clone on server**
```bash
ssh user@server
git clone https://github.com/YOUR_USERNAME/ML-Ops-project.git
cd ML-Ops-project
```

2. **Install Docker**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
apt install docker-compose -y
```

3. **Start**
```bash
docker-compose up -d
```

4. **Public access**
```
http://YOUR_SERVER_IP:3001
```

### With a domain name

See complete deployment documentation (contact me for more info).

---

## 📈 Performance

### Model

- **Architecture**: CNN (3 Conv2D + MaxPool blocks)
- **Parameters**: ~14.8M
- **Accuracy**: ~95% (validation)
- **Inference time**: ~200-500ms per image

### Scalability

- **API**: FastAPI (async, high performance)
- **Containerization**: Docker (easy to scale)
- **Storage**: MinIO (S3-compatible, distributed)

---

## 🤝 Contributing

This project was created as part of an MLOps course.

For any questions or suggestions, feel free to open an issue!

---

## 📝 License

This project is for educational purposes.

---

## 👤 Author

**Your Name**
- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [Your Profile](https://linkedin.com/in/your-profile)

---

## 🙏 Acknowledgments

- AlbertSchool for the MLOps course
- TensorFlow and Keras for the ML framework
- MLflow for MLOps tools
- FastAPI for the API framework
- React for the frontend framework

---

**Made with ❤️ for MLOps learning**

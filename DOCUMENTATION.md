# MLOps Project - Complete Documentation

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Quick Start Guide](#quick-start-guide)
3. [Project Architecture](#project-architecture)
4. [Testing & Results](#testing--results)
5. [Submission Checklist](#submission-checklist)
6. [CI/CD Setup](#cicd-setup)

---

## Executive Summary

### Project Overview

This MLOps project demonstrates a complete end-to-end machine learning pipeline for binary image classification (dandelion vs grass). The project showcases industry best practices in MLOps, including experiment tracking, model serving, containerization, and CI/CD automation.

### Key Features

- **High Performance Model**: 85% validation accuracy, 99%+ prediction confidence
- **Production-Ready API**: FastAPI with automatic documentation and health monitoring
- **Full MLOps Pipeline**: From data preprocessing to deployment
- **Experiment Tracking**: MLflow integration for reproducibility
- **Containerization**: Docker Compose for multi-service orchestration
- **Modern Frontend**: React TypeScript with real-time predictions
- **CI/CD**: GitHub Actions with self-hosted runners

### Technical Stack

- **ML Framework**: TensorFlow 2.16.1 / Keras
- **API**: FastAPI (async, high-performance)
- **Frontend**: React 18 + TypeScript + Vite
- **Tracking**: MLflow
- **Container**: Docker & Docker Compose
- **CI/CD**: GitHub Actions

---

## Quick Start Guide

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional)
- 4GB+ RAM
- Git & Git LFS

### Step 1: Clone and Setup

```bash
# Clone repository
git clone https://github.com/Andy-P626/ML-Ops-project.git
cd ML-Ops-project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Train Model (First Time Only)

```bash
# Download and prepare dataset
python run_import_clean.py

# Train model with MLflow tracking
python train_with_mlflow.py

# View MLflow experiments (optional)
mlflow ui --port 5000
```

### Step 3: Start API Server

```bash
# Start FastAPI server
cd api
python -m uvicorn main:app --reload --port 8000
```

API will be available at:
- **API Base**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Step 4: Test Predictions

Visit http://localhost:8000/docs and:

1. Click on `/predict` endpoint
2. Click "Try it out"
3. Upload an image from `cleaned_images_for_model/` folder
4. Click "Execute"
5. View prediction results with confidence scores

---

## Project Architecture

### System Overview

```
┌──────────────────────────────────────────────────────────────┐
│                     MLOps Pipeline                            │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Data Layer          Model Layer         Serving Layer       │
│  ┌─────────┐        ┌──────────┐        ┌──────────┐       │
│  │ 400 IMG │───────▶│   CNN    │───────▶│ FastAPI  │       │
│  │ 256x256 │        │14.8M prm │        │ REST API │       │
│  └─────────┘        └──────────┘        └──────────┘       │
│       │                   │                    │            │
│       ▼                   ▼                    ▼            │
│  ┌─────────┐        ┌──────────┐        ┌──────────┐       │
│  │Preproc  │        │  MLflow  │        │  React   │       │
│  │Pipeline │        │ Tracking │        │   UI     │       │
│  └─────────┘        └──────────┘        └──────────┘       │
│                                                               │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Docker Compose   │
                    │ Orchestration    │
                    └──────────────────┘
```

### Project Structure

```
ML-Ops-project/
├── api/
│   └── main.py                    # FastAPI application
├── Front/                         # React TypeScript frontend
│   ├── src/
│   │   ├── App.tsx               # Main application
│   │   └── components/           # UI components
│   └── package.json
├── cleaned_images_for_model/      # Training dataset (400 images)
├── mlruns/                        # MLflow experiment tracking
├── dandelion_grass_cnn.keras      # Trained model (170MB)
├── train_with_mlflow.py           # Training script
├── run_import_clean.py            # Data preparation
├── docker-compose.yml             # Multi-service setup
├── requirements.txt               # Dependencies
├── README.md                      # Main documentation
└── DOCUMENTATION.md               # This file
```

### API Endpoints

| Endpoint        | Method | Description                          |
| --------------- | ------ | ------------------------------------ |
| `/`             | GET    | API information                      |
| `/health`       | GET    | Health check & model status          |
| `/predict`      | POST   | Image classification                 |
| `/model-info`   | GET    | Model architecture details           |
| `/docs`         | GET    | Interactive API documentation        |

---

## Testing & Results

### Model Performance

| Metric                  | Value             |
| ----------------------- | ----------------- |
| Validation Accuracy     | 85%               |
| Training Accuracy       | 96%               |
| Model Size              | 170MB             |
| Total Parameters        | 14,839,105        |
| Training Time (CPU)     | ~13 minutes       |

### Prediction Results

| Test Image | Predicted Class | Confidence | Result     |
| ---------- | --------------- | ---------- | ---------- |
| Dandelion  | dandelion       | 99.99%     | ✅ Correct |
| Grass      | grass           | 99.74%     | ✅ Correct |

### Test Commands

```bash
# Health check
curl http://localhost:8000/health

# Model information
curl http://localhost:8000/model-info

# Prediction test
curl -X POST "http://localhost:8000/predict" \
  -F "file=@cleaned_images_for_model/dandelion_00000000.jpg"
```

### Expected Results

**Health Check Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_size": "170.12 MB",
  "classes": ["dandelion", "grass"]
}
```

**Prediction Response:**
```json
{
  "predicted_class": "dandelion",
  "confidence": 0.9999999953,
  "probabilities": {
    "dandelion": 0.9999999953,
    "grass": 4.678803846e-09
  },
  "timestamp": "2025-11-01T16:28:43.562732"
}
```

---

## Submission Checklist

### Required Components

- ✅ GitHub repository with complete code
- ✅ README.md with comprehensive documentation
- ✅ Working FastAPI server
- ✅ Trained CNN model (dandelion_grass_cnn.keras)
- ✅ Docker deployment configuration
- ✅ MLflow experiment tracking
- ✅ Test results and validation
- ✅ CI/CD pipelines (GitHub Actions)
- ✅ Frontend application (React TypeScript)

### Documentation Files

- ✅ README.md - Main project documentation
- ✅ DOCUMENTATION.md - Complete guide (this file)
- ✅ CICD_SETUP.md - CI/CD configuration guide
- ✅ report/Executive_Summary.md - Project summary
- ✅ report/Project_Presentation.md - Presentation materials
- ✅ report/Project_Testing_Report.md - Testing documentation
- ✅ report/Quick_Reference_Guide.md - Quick reference

### Screenshots & Demos

Required screenshots location: `report/screenshots_demo/`

1. **API Health Check** - `/health` endpoint response
2. **Model Info** - `/model-info` endpoint showing architecture
3. **Dandelion Prediction** - Successful dandelion classification
4. **Grass Prediction** - Successful grass classification
5. **MLflow UI** - Experiment tracking dashboard
6. **Docker Compose** - Multi-service running
7. **Frontend Demo** - React application in action

### Pre-Submission Checklist

- [ ] All code is committed and pushed to GitHub
- [ ] Model training runs successfully from scratch
- [ ] API server starts without errors
- [ ] All endpoints respond correctly
- [ ] Docker Compose builds and runs
- [ ] MLflow tracking is functional
- [ ] Frontend builds and runs
- [ ] CI/CD pipelines are configured
- [ ] All documentation is complete
- [ ] Screenshots are captured and saved

---

## CI/CD Setup

### GitHub Actions Workflows

This project uses GitHub Actions with self-hosted runners for CI/CD automation.

#### 1. CI/CD Pipeline (`.github/workflows/ci-cd.yml`)

**Triggers:**
- Push to main branch
- Pull requests

**Jobs:**
- Code quality checks (linting, formatting)
- Dependency installation
- Model validation
- API testing
- Docker image building
- Deployment to self-hosted environment

#### 2. Model Training Pipeline (`.github/workflows/model-training.yml`)

**Triggers:**
- Manual workflow dispatch
- Scheduled (optional)

**Parameters:**
- Epochs (default: 10)
- Batch size (default: 32)
- Learning rate (default: 0.001)

**Jobs:**
- Data preparation
- Model training with MLflow
- Model evaluation
- Artifact upload to MLflow

### Setting Up Self-Hosted Runner

**Step 1: Navigate to Repository Settings**
1. Go to your GitHub repository
2. Click **Settings** → **Actions** → **Runners**
3. Click **New self-hosted runner**

**Step 2: Download and Configure Runner**

```bash
# Create directory for runner
mkdir actions-runner && cd actions-runner

# Download runner (follow GitHub's specific download link)
# Example for macOS:
curl -o actions-runner-osx-x64-2.311.0.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-osx-x64-2.311.0.tar.gz

# Extract
tar xzf ./actions-runner-osx-x64-2.311.0.tar.gz

# Configure (use token from GitHub)
./config.sh --url https://github.com/Andy-P626/ML-Ops-project --token YOUR_TOKEN
```

**Step 3: Start Runner**

```bash
# Start runner interactively
./run.sh

# Or install as service (macOS)
./svc.sh install
./svc.sh start
```

**Step 4: Verify Runner**
- Check **Settings** → **Actions** → **Runners**
- Runner should show as "Idle" (green)

### Monitoring CI/CD

- **Actions Dashboard**: https://github.com/Andy-P626/ML-Ops-project/actions
- **CI/CD Runs**: View all pipeline executions
- **Training Runs**: Monitor model training jobs
- **Logs**: Detailed execution logs for debugging

### Workflow Files Location

```
.github/
└── workflows/
    ├── ci-cd.yml              # Main CI/CD pipeline
    └── model-training.yml     # Model training automation
```

---

## Docker Deployment

### Quick Start with Docker Compose

```bash
# Start all services
docker-compose up --build

# Services available at:
# - API:       http://localhost:8000
# - Frontend:  http://localhost:3000
# - MLflow:    http://localhost:5000
# - Minio:     http://localhost:9001
```

### Individual Service Deployment

```bash
# Build API image
docker build -t mlops-api:latest -f Dockerfile.api .

# Run API container
docker run -p 8000:8000 mlops-api:latest

# Build Frontend
cd Front
docker build -t mlops-frontend:latest .
docker run -p 3000:3000 mlops-frontend:latest
```

---

## Troubleshooting

### Common Issues

**Issue: Model file not found**
```bash
# Solution: Train the model first
python run_import_clean.py
python train_with_mlflow.py
```

**Issue: API fails to start**
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill process if needed
kill -9 <PID>
```

**Issue: Dependencies not installing**
```bash
# Upgrade pip first
pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v
```

**Issue: Docker build fails**
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

---

## MLOps Best Practices Implemented

### ✅ Data Management
- Automated data download and preprocessing
- Version-controlled datasets
- Balanced dataset (200 dandelions + 200 grass)
- Consistent preprocessing pipeline

### ✅ Experiment Tracking
- MLflow integration for all training runs
- Automatic logging of parameters and metrics
- Model artifact versioning
- Reproducible experiments

### ✅ Model Versioning
- Git LFS for large model files
- MLflow model registry
- Semantic versioning
- Model lineage tracking

### ✅ API Development
- RESTful design principles
- Automatic OpenAPI documentation
- Input validation with Pydantic
- Comprehensive error handling
- Health monitoring endpoints

### ✅ Containerization
- Docker for reproducible environments
- Multi-stage builds for optimization
- Docker Compose for orchestration
- Environment variable configuration

### ✅ CI/CD Automation
- Automated testing on commits
- Continuous deployment pipeline
- Model training workflows
- Self-hosted runner integration

### ✅ Testing & Validation
- API endpoint testing
- Model inference validation
- Performance benchmarking
- Health check monitoring

---

## Additional Resources

### Documentation
- [README.md](README.md) - Main project overview
- [CICD_SETUP.md](CICD_SETUP.md) - Detailed CI/CD guide
- [Front/README.md](Front/README.md) - Frontend documentation

### Reports
- [Executive Summary](report/Executive_Summary.md)
- [Project Presentation](report/Project_Presentation.md)
- [Testing Report](report/Project_Testing_Report.md)
- [Quick Reference](report/Quick_Reference_Guide.md)

### External Links
- **GitHub Repository**: https://github.com/Andy-P626/ML-Ops-project
- **MLflow Docs**: https://mlflow.org/docs/latest/index.html
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **TensorFlow Guides**: https://www.tensorflow.org/guide

---

## License

MIT License - See [LICENSE](LICENSE) file for details

---

## Contact

**Project Repository**: https://github.com/Andy-P626/ML-Ops-project

For questions or issues, please open an issue on GitHub.

---

*Last Updated: November 1, 2025*
*Version: 1.0.0*

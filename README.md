# 🌿 ML-Ops Project: Dandelion vs Grass Classification

## 📌 Overview

This repository contains an end-to-end ML Ops demo for binary plant classification: dandelion vs grass. It combines:

- A FastAPI-based prediction API with TensorFlow/Keras model loading
- A React + Vite frontend interface
- MLflow for experiment tracking and model registry
- MinIO as an S3-compatible artifact store
- Evidently AI for production performance and data drift monitoring
- Docker Compose orchestration for local development
- GitHub Actions for CI/CD automation

## 🏗️ Architecture

The project uses the following components:

- **Orchestration:** `docker-compose.yml` runs MinIO (object storage), MLflow (tracking/registry), API (FastAPI backend), and Frontend (React/Vite app).
- **API Backend:** `api/main.py` exposes endpoints for health checks and image classification.
- **Frontend:** A visual interface built with React to upload images and display predictions.
- **Monitoring:** `monitoring/run_monitoring.py` uses Evidently AI to calculate data drift, target drift, and classification metrics.

## Features

- Train a CNN model for binary classification using local image data
- Track experiments and model artifacts in MLflow
- Store MLflow artifacts securely in MinIO
- Serve predictions through a REST API with fallback mechanisms
- Monitor model performance and detect Data/Target Drift with Evidently AI
- Automated CI/CD pipelines for testing, building, and deployment

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ for local script execution
- Node.js 18+ and npm for local frontend development

## 🚀 Quick Start

### 1. Prepare the model
The API expects a trained model file at `models/dandelion_grass_cnn.keras`.
If you do not have the model yet, train it locally:
python retrain/train_with_mlflow.py

### 2. Start the full stack with Docker Compose
```bash 
docker-compose up --build
```
After startup, the services will be available at:

Frontend: http://localhost:3001

API docs: http://localhost:8000/docs

MLflow UI: http://localhost:5000

MinIO Console: http://localhost:9001

### 3. Run API locally (optional)
Bash
./scripts/start_api.sh
### 4. Run frontend locally (optional)
Bash
./scripts/start_frontend.sh

## API Endpoints
GET / - Root info and endpoint summary

GET /health - Health check (reports model load status for infrastructure monitoring)

POST /predict - Upload an image and receive prediction results

## MLflow & Model Registry
The project uses MLflow and an S3-compatible MinIO backend for artifact storage.

MLflow tracking: http://localhost:5000

Default artifact root: s3://mlflow-artifacts/

MinIO console: http://localhost:9001

Useful model lifecycle scripts (located in /retrain and /monitoring):

register_model_simple.py - Register the local model with MLflow

promote_model_to_production.py - Promote a registered model version to Production

setup_minio_bucket.py - Create and validate the mlflow-artifacts bucket in MinIO

## Monitoring in Production (Evidently AI)
To ensure the model remains reliable in production, this project uses Evidently AI to monitor performance and detect anomalies.

Run the monitoring pipeline:

Bash
python monitoring/run_monitoring.py
### or use the shell entrypoint: ./monitoring/run_monitoring.sh
This script compares reference training data against current production data to compute:

Data Drift: Detects shifts in input features (e.g., image brightness, dimensions).

Target Drift: Detects shifts in the distribution of model predictions.

Classification Metrics: Calculates Accuracy, F1-Score, and generates a Confusion Matrix.

The output is an interactive HTML report saved at monitoring/evidently_report.html.

## CI/CD Pipelines
This repository includes automation workflows defined in .github/workflows.

Continuous Integration & Deployment (ci-cd.yml):

Triggered on push and pull_request to main and develop.

Installs Python dependencies, runs linting, and executes unit tests (e.g., tests/test_api.py).

Builds and validates the React frontend using Node.js and Vite.

Builds Docker production images upon successful validation.

Continuous Training (model-training.yml):

Triggered manually via workflow_dispatch.

Automates data preparation, model retraining, and MLflow tracking.

Uploads the new model artifacts as GitHub workflow artifacts.

## Repository Layout
api/ - FastAPI application code

Front/ - React/Vite frontend app

models/ - Trained model files (e.g., .keras)

monitoring/ - Evidently AI scripts and HTML reports

notebooks/ - Jupyter notebooks for Exploratory Data Analysis (EDA)

retrain/ - Scripts for model training and MLflow registry promotion

scripts/ - Shell utilities for local execution

src/ - Source code for data preprocessing and cleaning

tests/ - Unit tests for the API and model validation

docker-compose.yml - Local stack orchestration

Dockerfile.api & Front/Dockerfile - Container build configurations

## License
MIT License
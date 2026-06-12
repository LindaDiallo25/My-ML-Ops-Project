# ML-Ops Project

## Overview

This repository contains an end-to-end ML Ops demo for binary plant classification: dandelion vs grass. It combines:

- A FastAPI-based prediction API with TensorFlow/Keras model loading
- A React + Vite frontend interface
- MLflow for experiment tracking and model registry
- MinIO as an S3-compatible artifact store
- Docker Compose orchestration for local development

## Architecture

The project uses the following components:

- `docker-compose.yml` to orchestrate:
  - `minio` for object storage
  - `mlflow` for tracking and model registry
  - `api` serving the plant classification endpoint
  - `frontend` serving the web application
- `api/main.py` FastAPI app exposing `/predict`, `/health`, and OpenAPI docs at `/docs`
- `scripts/train_with_mlflow.py` to train the CNN model and log artifacts to MLflow
- `models/dandelion_grass_cnn.keras` stored locally and mounted into the API container
- `Front/` containing the frontend app built with React and Vite

## Features

- Train a CNN model for binary classification using local image data
- Track experiments and model artifacts in MLflow
- Store MLflow artifacts in MinIO
- Serve predictions through a REST API
- Visual frontend for uploading images and displaying predictions

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ for local script execution
- Node.js 18+ and npm for local frontend development

## Quick Start

### 1. Prepare the model

The API expects a trained model file at `models/dandelion_grass_cnn.keras`.

If you do not have the model yet, train it locally:

```bash
python scripts/train_with_mlflow.py
```

This script loads cleaned images from `data/images`, trains the CNN, saves the model to `models/dandelion_grass_cnn.keras`, and logs the run to MLflow.

### 2. Start the full stack with Docker Compose

```bash
docker-compose up --build
```

After startup, the services will be available at:

- Frontend: `http://localhost:3001`
- API docs: `http://localhost:8000/docs`
- MLflow UI: `http://localhost:5000`
- MinIO Console: `http://localhost:9001`

### 3. Run API locally (optional)

```bash
./scripts/start_api.sh
```

This starts the FastAPI server on `http://localhost:8000` and provides the API documentation at `/docs`.

### 4. Run frontend locally (optional)

```bash
./scripts/start_frontend.sh
```

The frontend dev server is available at `http://localhost:5173`.

## API Endpoints

The main API endpoints are:

- `GET /` - root info and endpoint summary
- `GET /health` - health check (reports model load status)
- `POST /predict` - upload an image and receive prediction results

### Example prediction request

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/image.jpg"
```

## MLflow & Model Registry

The project uses MLflow and an S3-compatible MinIO backend for artifact storage.

- MLflow tracking: `http://localhost:5000`
- Default artifact root: `s3://mlflow-artifacts/`
- MinIO console: `http://localhost:9001`

Useful helper scripts:

- `scripts/register_model_simple.py` - register the local model with MLflow
- `scripts/promote_model_to_production.py` - promote a registered model version to Production
- `scripts/setup_minio_bucket.py` - create and validate the `mlflow-artifacts` bucket in MinIO

## Local development

### Install Python requirements

```bash
pip install -r requirements.txt
```

### Install frontend dependencies

```bash
cd Front
npm install
```

## Repository layout

- `api/` - FastAPI application code
- `Front/` - React/Vite frontend app
- `models/` - trained model files
- `data/images/` - training image dataset
- `scripts/` - training, deployment, and MLflow utilities
- `docker-compose.yml` - local stack orchestration
- `Dockerfile.api` - API container build config
- `Front/Dockerfile` - frontend production container build config

## Notes

- The API will attempt to load the model from MLflow registry first, then fallback to the local `models/dandelion_grass_cnn.keras` file.
- If the model file is missing, the API returns `503 Service Unavailable` for prediction requests.
- For production use, update CORS settings, secrets, and host validation.

## CI/CD Pipelines

This repository includes automation workflows defined in `.github/workflows`.

- `.github/workflows/ci-cd.yml`
  - Runs on `push` to `main` and `develop`, and on pull request creation targeting `main`.
  - Verifies the API with Python dependency installation, linting, import tests, and endpoint checks.
  - Builds and validates the frontend using Node.js and Vite.
  - Builds Docker images for production deployment on successful `main` pushes.

- `.github/workflows/model-training.yml`
  - Triggered manually via `workflow_dispatch`.
  - Installs Python dependencies, prepares training data, and trains the CNN model with MLflow tracking.
  - Uploads the trained model and MLflow artifacts as GitHub workflow artifacts.

Notes on CI/CD behavior:

- The API pipeline uses a self-hosted runner environment and PowerShell-based job steps.
- Frontend validation builds the Vite app and ensures `Front/build` exists.
- Docker image creation is gated behind successful API and frontend validation and runs only on `main` branch push events.

## License

This repository does not include a license file. Add a license if you plan to open-source or share the project publicly.


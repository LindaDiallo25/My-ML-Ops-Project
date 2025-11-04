# 🚀 MLOps Project Quick Reference Guide

## ⚡ Quick Start Steps

### 1️⃣ Environment Setup (First Time)
```bash
# Navigate to project directory
cd "/Users/shellychang/Library/CloudStorage/GoogleDrive-shuhc121@gmail.com/我的雲端硬碟/Albertschool_M2_1/as_m2-1/ML Ops/MLOP_project/ML-Ops-project"

# Activate virtual environment
source venv/bin/activate

# Install dependencies (if not already installed)
pip install -r requirements.txt
```

### 2️⃣ Train Model (Must Execute First)
```bash
# Method 1: Basic training
python run_train_model.py

# Method 2: Using MLflow tracking (recommended)
python train_with_mlflow.py
```

⏱️ **Estimated Time**: 10-15 minutes  
📊 **Output**: `dandelion_grass_cnn.keras` (approximately 170MB)

### 3️⃣ Start API Service
```bash
# Using startup script (recommended)
./start_api.sh

# Or manual startup
cd api
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

✅ **Check**: Open http://localhost:8000/docs

### 4️⃣ Start Frontend (New Terminal)
```bash
# Using startup script (recommended)
./start_frontend.sh

# Or manual startup
cd Front
npm install  # First time only
npm run dev
```

✅ **Check**: Open http://localhost:5173

---

## 🧪 Testing Commands

### API Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2025-11-01T..."
}
```

### Test Image Prediction
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@cleaned_images_for_model/dandelion_00000000.jpg"
```

Expected response:
```json
{
  "predicted_class": "dandelion",
  "confidence": 0.92,
  "probabilities": {
    "dandelion": 0.92,
    "grass": 0.08
  }
}
```

---

## 🐳 Docker Deployment

### Start All Services
```bash
docker-compose up --build
```

### Service Ports
- Frontend: http://localhost:3000
- API: http://localhost:8000
- MLflow: http://localhost:5000
- Minio: http://localhost:9001

### Stop Services
```bash
docker-compose down
```

---

## 🔧 Troubleshooting

### ❌ Issue 1: Model Not Loaded
```bash
# Check model file size
ls -lh dandelion_grass_cnn.keras

# If only 134 bytes, need to retrain
python run_train_model.py
```

### ❌ Issue 2: Port Already in Use
```bash
# Release port 8000
lsof -ti:8000 | xargs kill -9

# Release port 5173
lsof -ti:5173 | xargs kill -9
```

### ❌ Issue 3: Missing Dependencies
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### ❌ Issue 4: npm Install Failure
```bash
cd Front
rm -rf node_modules package-lock.json
npm install
```

---

## 📊 MLflow Usage

### Start MLflow UI
```bash
mlflow ui --host 0.0.0.0 --port 5000
```

Visit: http://localhost:5000

### View Experiments
- Experiment name: `dandelion_grass_classification`
- Logged metrics: accuracy, loss, val_accuracy, val_loss
- Saved parameters: epochs, batch_size, image_size, etc.

---

## 📁 Important File Locations

### Model-related
```
dandelion_grass_cnn.keras          # Trained model
training_history.png               # Training curves
mlruns/                           # MLflow experiment logs
```

### Data-related
```
cleaned_images_for_model/         # Training data (400 images)
image_data_from_repo/             # Raw downloaded data
```

### Code
```
api/main.py                       # FastAPI main program
train_with_mlflow.py              # Training script
run_import_clean.py               # Data processing script
Front/src/App.tsx                 # Frontend main program
```

### Configuration
```
requirements.txt                  # Python dependencies
docker-compose.yml                # Docker service config
Dockerfile.api                    # API container config
Front/package.json                # Frontend dependencies
```

---

## 🎯 Testing Checklist

### Basic Functionality Tests
- [ ] Model training successful
- [ ] Model file size correct (~170MB)
- [ ] API starts without errors
- [ ] API health check passes
- [ ] Swagger docs accessible
- [ ] Frontend starts without errors
- [ ] Frontend page displays normally

### Feature Tests
- [ ] Can upload images
- [ ] Prediction results correct
- [ ] Confidence display normal
- [ ] Error handling works
- [ ] Can repeat predictions

### Advanced Tests
- [ ] MLflow UI accessible
- [ ] Docker Compose starts successfully
- [ ] All service communications normal

---

## 📸 Demo Recording Points

### 1. Demonstrate Data Processing
```bash
python run_import_clean.py
```
- Show automated download
- Show image cleaning process

### 2. Demonstrate Model Training
```bash
python train_with_mlflow.py
```
- Show training progress
- Show MLflow UI
- Show training curves

### 3. Demonstrate API Service
- Visit http://localhost:8000/docs
- Test `/predict` endpoint
- Show JSON response

### 4. Demonstrate Web App
- Upload dandelion image
- Upload grass image
- Show prediction results

### 5. Demonstrate Docker Deployment
```bash
docker-compose up
```
- Show all services starting
- Show service integration

---

## 💡 Project Highlights (Presentation Points)

### Technical Highlights
✨ **Complete MLOps Pipeline**  
✨ **Modern Technology Stack** (FastAPI, React, Docker)  
✨ **Experiment Tracking** (MLflow)  
✨ **Containerized Deployment** (Docker Compose)  
✨ **Auto-generated API Documentation** (Swagger)  

### Feature Highlights
✨ **Automated Data Processing**  
✨ **85% Classification Accuracy**  
✨ **Real-time Prediction API**  
✨ **User-friendly Web Interface**  
✨ **Drag-and-drop Upload**  

### Engineering Highlights
✨ **Clear Code Structure**  
✨ **Comprehensive Error Handling**  
✨ **Detailed Documentation**  
✨ **Reproducible Experiments**  
✨ **Production-ready**  

---

## 📞 Support Resources

### Generated Documents
1. `Project_Testing_Report.md` - Detailed test results
2. `Project_Presentation.md` - Complete presentation content
3. `Executive_Summary.md` - Execution summary
4. `Quick_Reference_Guide.md` - This document

### Original Documents
- `README.md` - Complete project description
- `QUICKSTART.md` - Quick start
- `START_HERE.md` - Getting started guide
- `SUBMISSION_CHECKLIST.md` - Submission checklist

---

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| Environment setup | 5 minutes |
| Model training | 10-15 minutes |
| API startup | 1 minute |
| Frontend startup | 2 minutes |
| Feature testing | 5 minutes |
| Docker deployment | 5 minutes |
| **Total** | **30-35 minutes** |

---

## ✅ Completion Criteria

Project is ready for demonstration when all the following conditions are met:

1. ✅ Model file > 100MB
2. ✅ API returns `model_loaded: true`
3. ✅ Frontend can upload and predict
4. ✅ Prediction results reasonable (confidence > 50%)
5. ✅ No console errors

---

**Good luck with testing!** 🎉

For questions, refer to the testing report or original README.

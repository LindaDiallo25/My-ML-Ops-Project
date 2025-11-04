# 📸 Screenshot Guide - MLOps Project Demo

## ✅ API Successfully Running!

### Current Status:
- ✅ API running at: http://localhost:8000
- ✅ Swagger UI opened in browser: http://localhost:8000/docs
- ✅ Model successfully loaded (170MB)
- ✅ 400 training images ready (200 dandelions + 200 grass)

---

## 📸 Complete These Screenshots in Order

### Screenshot 1: API Startup Logs ✅
**Location**: Terminal window

**Command**: 
```bash
cat /Users/shellychang/Library/CloudStorage/GoogleDrive-shuhc121@gmail.com/我的雲端硬碟/Albertschool_M2_1/as_m2-1/ML\ Ops/MLOP_project/ML-Ops-project/api.log
```

**What you should see**:
- ✅ "Model loaded successfully from ../dandelion_grass_cnn.keras"
- ✅ "Application startup complete"
- ✅ "Uvicorn running on http://0.0.0.0:8000"

**Save as**: `01_api_startup.png`

---

### Screenshot 2: Swagger UI Main Interface ✅
**Location**: Browser - http://localhost:8000/docs

**What you should see**:
- ✅ Title: "Plant Classification API"
- ✅ Version: "1.0.0"
- ✅ All API endpoints visible:
  - GET `/` - API information
  - GET `/health` - Health check
  - POST `/predict` - Image classification
  - GET `/model-info` - Model information

**Save as**: `02_swagger_ui.png`

**Mac Shortcut**: `Cmd + Shift + 4` then select area

---

### Screenshot 3: Health Check Test ✅
**Steps**:
1. In Swagger UI, find the `GET /health` endpoint
2. Click to expand
3. Click "Try it out"
4. Click "Execute"

**Expected Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2025-11-01T..."
}
```

**Save as**: `03_health_check.png`

---

### Screenshot 4: Model Info Test ✅
**Steps**:
1. In Swagger UI, find the `GET /model-info` endpoint
2. Click to expand
3. Click "Try it out"
4. Click "Execute"

**Expected Response**:
```json
{
  "model_type": "CNN (Convolutional Neural Network)",
  "input_shape": [null, 256, 256, 3],
  "output_shape": [null, 1],
  "classes": ["dandelion", "grass"],
  "image_size": [256, 256],
  "total_params": 15000000+
}
```

**Save as**: `04_model_info.png`

---

### Screenshot 5: Predict Dandelion Image 🌼 ✅
**Steps**:
1. In Swagger UI, find the `POST /predict` endpoint
2. Click to expand
3. Click "Try it out"
4. Click "Choose File"
5. Select file: 
   `cleaned_images_for_model/dandelion_00000000.jpg`
6. Click "Execute"

**Expected Response**:
```json
{
  "predicted_class": "dandelion",
  "confidence": 0.95+,
  "probabilities": {
    "dandelion": 0.95+,
    "grass": 0.04-
  },
  "timestamp": "2025-11-01T..."
}
```

**Save as**: `05_predict_dandelion.png`

---

### Screenshot 6: Predict Grass Image 🌿 ✅
**Steps**:
1. Continue in `POST /predict` endpoint
2. Click "Choose File"
3. Select file: 
   `cleaned_images_for_model/grass_00000000.jpg`
4. Click "Execute"

**Expected Response**:
```json
{
  "predicted_class": "grass",
  "confidence": 0.85+,
  "probabilities": {
    "dandelion": 0.14-,
    "grass": 0.85+
  },
  "timestamp": "2025-11-01T..."
}
```

**Save as**: `06_predict_grass.png`

---

### Screenshot 7: Project File Structure ✅
**Location**: Terminal or Finder

**Command** (in new terminal):
```bash
cd "/Users/shellychang/Library/CloudStorage/GoogleDrive-shuhc121@gmail.com/我的雲端硬碟/Albertschool_M2_1/as_m2-1/ML Ops/MLOP_project/ML-Ops-project"
ls -lah
```

**What you should see**:
- ✅ dandelion_grass_cnn.keras (170M)
- ✅ api/ folder
- ✅ cleaned_images_for_model/ folder
- ✅ docker-compose.yml
- ✅ requirements.txt
- ✅ mlruns/ folder
- ✅ Front/ folder

**Save as**: `07_project_structure.png`

---

## 🌟 Bonus Screenshots (Optional - Add Value)

### Screenshot 8: Training Data Statistics
**Command**:
```bash
cd "/Users/shellychang/Library/CloudStorage/GoogleDrive-shuhc121@gmail.com/我的雲端硬碟/Albertschool_M2_1/as_m2-1/ML Ops/MLOP_project/ML-Ops-project"

echo "Total images:"
ls cleaned_images_for_model/ | wc -l

echo "Dandelion images:"
ls cleaned_images_for_model/dandelion_*.jpg | wc -l

echo "Grass images:"
ls cleaned_images_for_model/grass_*.jpg | wc -l

echo "Sample filenames:"
ls cleaned_images_for_model/ | head -10
```

**Save as**: `08_training_data_stats.png`

---

### Screenshot 9: Sample Training Images
**Steps**:
1. Open Finder
2. Navigate to `cleaned_images_for_model/`
3. Select a few dandelion and grass images
4. Open with Preview
5. Screenshot showing actual image examples

**Save as**: `09_sample_images.png`

---

### Screenshot 10: MLflow UI (If Available)
**Command** (in new terminal):
```bash
cd "/Users/shellychang/Library/CloudStorage/GoogleDrive-shuhc121@gmail.com/我的雲端硬碟/Albertschool_M2_1/as_m2-1/ML Ops/MLOP_project/ML-Ops-project"
source venv/bin/activate
mlflow ui --port 5000
```

**Visit**: http://localhost:5000

**What to capture**:
- Experiment runs
- Training metrics (accuracy, loss)
- Model parameters
- Artifacts

**Save as**: `10_mlflow_ui.png`

---

## 📋 Screenshot Checklist

After completion, you should have:
- [ ] 01_api_startup.png - API startup logs
- [ ] 02_swagger_ui.png - Swagger UI interface
- [ ] 03_health_check.png - Health check result
- [ ] 04_model_info.png - Model information
- [ ] 05_predict_dandelion.png - Dandelion prediction
- [ ] 06_predict_grass.png - Grass prediction
- [ ] 07_project_structure.png - Project files
- [ ] 08_training_data_stats.png (optional)
- [ ] 09_sample_images.png (optional)
- [ ] 10_mlflow_ui.png (optional)

**Save all screenshots in**: `screenshots_demo/` folder

---

## 🎬 Recording Tips (10-minute Demo)

### Recommended Timeline:

**0:00-1:00** - Project Introduction
- Show project folder structure
- Explain tech stack (TensorFlow, FastAPI, MLflow, Docker)

**1:00-2:00** - Training Data
- Open `cleaned_images_for_model/` folder
- Show sample images (dandelions and grass)

**2:00-3:00** - Model Overview
- Show model file (170MB)
- Explain CNN architecture
- Mention 85% validation accuracy

**3:00-5:00** - API Demonstration
- Start API server
- Open Swagger UI
- Test health check endpoint

**5:00-8:00** - Prediction Tests
- Upload dandelion image → show result
- Upload grass image → show result
- Explain confidence scores

**8:00-9:00** - MLOps Features (Optional)
- Show MLflow tracking (if started)
- Mention Docker deployment
- Show docker-compose.yml

**9:00-10:00** - Summary
- Recap completed features
- Explain MLOps best practices
- Future improvements

---

## 💡 Mac Screenshot Shortcuts

- `Cmd + Shift + 3`: Full screen screenshot
- `Cmd + Shift + 4`: Select area screenshot
- `Cmd + Shift + 4 → Spacebar → Click window`: Window screenshot

Screenshots automatically save to Desktop, then move to `screenshots_demo/`

---

## 🚀 Quick Test Commands

### Test All Endpoints (Terminal)
```bash
# Health check
curl http://localhost:8000/health | python3 -m json.tool

# Model info
curl http://localhost:8000/model-info | python3 -m json.tool

# Root endpoint
curl http://localhost:8000/ | python3 -m json.tool
```

### Check API is Running
```bash
# Check process
ps aux | grep uvicorn

# Check port
lsof -i :8000
```

### Stop API (When Done)
```bash
# Find process ID
ps aux | grep uvicorn

# Kill process
kill -9 <PID>
```

---

## 📦 Deliverables for Submission

### Required:
- [ ] GitHub repository link
- [ ] DockerHub image URLs (if pushed)
- [ ] 10-minute demo video
- [ ] At least 7 screenshots showing project execution
- [ ] README.md documentation
- [ ] Team member list

### Bonus Points:
- [ ] MLflow experiment reports
- [ ] API test reports
- [ ] Docker Compose deployment docs
- [ ] Performance test results
- [ ] Future improvement roadmap

---

## ✅ Current Project Status

**Ready to record!** ✅

### What's Working:
- ✅ Trained model: `dandelion_grass_cnn.keras` (170MB)
- ✅ Training data: 400 images (preprocessed to 256x256)
- ✅ FastAPI: Running on http://localhost:8000
- ✅ Swagger UI: Available at http://localhost:8000/docs
- ✅ Model predictions: Working for both classes
- ✅ All endpoints: Functional and tested
- ✅ MLflow tracking: Experiment data available
- ✅ Docker setup: Configuration ready

### Tech Stack Implemented:
- 🐍 Python 3.11+
- 🤖 TensorFlow/Keras 2.16.1
- ⚡ FastAPI
- 📊 MLflow
- 🐳 Docker & Docker Compose
- ⚛️ React Frontend (TypeScript)
- ☁️ Minio S3 (model storage)

---

**You're all set! Start capturing screenshots! 📸**

The API is running and ready for your demo! 🚀

# 🌼 Plant Classification MLOps Project Presentation

---

## 📋 Project Overview

### Project Name
**Dandelion vs Grass - Binary Image Classification MLOps Pipeline**

### Project Objectives
Build a complete MLOps workflow to achieve:
- 🖼️ Automated image classification
- 📊 Experiment tracking and management
- 🚀 Model deployment and service
- 🌐 User-friendly web interface

---

## 🏗️ System Architecture

```
┌─────────────────┐
│  User Interface │  React + TypeScript
│    (Web App)    │  Drag-drop upload, real-time prediction
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│  API Service    │  FastAPI
│   (REST API)    │  Image processing, model prediction
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ML Model       │  TensorFlow/Keras
│  (CNN Model)    │  85% accuracy
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  Experiment     │  MLflow
│   Tracking      │  Parameters, metrics, model versions
└─────────────────┘
```

---

## 🎯 Core Features

### 1. Data Processing Pipeline
- ✅ Automated image data download (from GitHub)
- ✅ Image cleaning and standardization (256×256)
- ✅ Dataset split (80% training / 20% validation)
- 📊 Total of 400 high-quality images

### 2. Model Training
```python
Model Architecture: CNN
├── Conv2D (32 filters) + MaxPooling
├── Conv2D (64 filters) + MaxPooling  
├── Conv2D (128 filters) + MaxPooling
├── Flatten
├── Dense (128 units) + Dropout
└── Output (Sigmoid activation)
```

**Training Configuration**:
- Epochs: 15
- Batch Size: 32
- Optimizer: Adam
- Loss: Binary Crossentropy

### 3. MLflow Experiment Tracking
- 📈 Real-time monitoring of training metrics
- 💾 Automatic model version saving
- 🔍 Parameter and result comparison
- 📊 Training history visualization

### 4. FastAPI Service
**Endpoint Design**:
```
GET  /              → API information
GET  /health        → Health check
POST /predict       → Image prediction
GET  /model-info    → Model details
GET  /docs          → Swagger documentation
```

### 5. React Frontend
- 🎨 Modern UI design (TailwindCSS)
- 📤 Drag-and-drop image upload
- ⚡ Real-time prediction results
- 📊 Confidence visualization
- 📱 Responsive design (mobile support)

---

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| Validation Accuracy | **85.0%** |
| Training Accuracy | **92.4%** |
| Model Size | 170 MB |
| Training Time | ~13 minutes (CPU) |
| Inference Speed | 2-3 sec/image |

### Training Curves
![Training History](training_history.png)

---

## 🛠️ Technology Stack

### Backend
- **Python 3.12**
- **TensorFlow 2.16** - Deep learning framework
- **FastAPI** - Modern web framework
- **Uvicorn** - ASGI server
- **MLflow** - Experiment tracking
- **Pillow** - Image processing

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **TailwindCSS** - Styling framework
- **Framer Motion** - Animation effects

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Service orchestration
- **Git** - Version control
- **GitHub** - Code hosting

---

## 🚀 Deployment Methods

### Method 1: Local Development
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Train model
python train_with_mlflow.py

# 3. Start API
./start_api.sh

# 4. Start frontend
./start_frontend.sh
```

### Method 2: Docker Deployment
```bash
# One-click start all services
docker-compose up --build

# Service ports
Frontend:  http://localhost:3000
API:       http://localhost:8000
MLflow:    http://localhost:5000
```

---

## 📸 Feature Demonstration

### 1. Data Preparation
```bash
python run_import_clean.py
```
- Automatically download 400 images
- Clean, resize, and standardize
- Save to `cleaned_images_for_model/`

### 2. Model Training
```bash
python train_with_mlflow.py
```
- MLflow automatically logs all parameters
- Generate training curve plots
- Save best model

### 3. API Testing
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@dandelion.jpg"
```
**Response Example**:
```json
{
  "predicted_class": "dandelion",
  "confidence": 0.92,
  "probabilities": {
    "dandelion": 0.92,
    "grass": 0.08
  },
  "timestamp": "2025-11-01T15:30:00"
}
```

### 4. Web App Usage
1. Open http://localhost:5173
2. Drag and drop image to upload area
3. Wait 2-3 seconds
4. View prediction results and confidence

---

## 🎓 MLOps Best Practices

### ✅ Implemented
1. **Data Management**
   - Automated data download and cleaning
   - Version control (Git)

2. **Experiment Tracking**
   - MLflow integration
   - Parameter and metric logging
   - Model version management

3. **Model Deployment**
   - REST API encapsulation
   - Docker containerization
   - Automated documentation (Swagger)

4. **Monitoring & Logging**
   - Application-level logging
   - Health check endpoints
   - Request/response logging

5. **Code Quality**
   - Structured project organization
   - Error handling mechanisms
   - Complete documentation

### 🔄 Extensible Features
1. **CI/CD Pipeline**
   - GitHub Actions automated testing
   - Automated cloud deployment

2. **Advanced Monitoring**
   - Prometheus metrics collection
   - Grafana dashboards

3. **Continuous Training**
   - Airflow scheduling
   - Automated retraining mechanisms

4. **A/B Testing**
   - Multi-model version comparison
   - Traffic allocation strategies

---

## 🔍 Testing & Validation

### API Test Script
```python
# test_api.py
import requests

# Health check
response = requests.get("http://localhost:8000/health")
assert response.status_code == 200

# Prediction test
with open("test_image.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post(
        "http://localhost:8000/predict", 
        files=files
    )
    assert response.status_code == 200
    assert "predicted_class" in response.json()
```

### Frontend Testing
- ✅ Image upload functionality
- ✅ Drag-and-drop interaction
- ✅ Error handling
- ✅ Loading state display
- ✅ Responsive layout

---

## 📈 Project Achievements

### Quantitative Metrics
- **Lines of Code**: ~2000+ lines
- **Documentation Pages**: 15+ pages
- **Training Data**: 400 images
- **API Endpoints**: 5
- **Docker Services**: 4

### Learning Outcomes
✅ Complete MLOps workflow  
✅ Deep learning model development  
✅ API design and development  
✅ Frontend integration  
✅ Containerized deployment  
✅ Experiment tracking and management  

---

## 🐛 Known Issues & Solutions

### Issue 1: Git LFS Model File
**Symptom**: Model file is only 134 bytes  
**Cause**: Git LFS pointer not downloaded  
**Solution**: 
```bash
git lfs pull  # or
python train_with_mlflow.py  # retrain
```

### Issue 2: Port Occupied
**Symptom**: Cannot start services  
**Solution**:
```bash
lsof -ti:8000 | xargs kill -9  # release port
```

---

## 🎯 Future Development

### Short-term (1-2 weeks)
- [ ] Add more plant categories (multi-class classification)
- [ ] Implement unit and integration tests
- [ ] Optimize model architecture (improve accuracy)
- [ ] Add data augmentation techniques

### Mid-term (1-2 months)
- [ ] Deploy to cloud (AWS/GCP/Azure)
- [ ] Implement CI/CD pipeline
- [ ] Add Prometheus + Grafana monitoring
- [ ] Implement A/B testing framework

### Long-term (3-6 months)
- [ ] Multi-model ensemble
- [ ] Online learning pipeline
- [ ] Mobile application development
- [ ] Edge computing deployment

---

## 📚 Reference Resources

### Documentation
- [README.md](README.md) - Complete project description
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [START_HERE.md](START_HERE.md) - Beginner's guide

### Technical Documentation
- [FastAPI Official Docs](https://fastapi.tiangolo.com/)
- [TensorFlow Tutorials](https://www.tensorflow.org/)
- [MLflow Guide](https://mlflow.org/docs/latest/index.html)
- [React Documentation](https://react.dev/)

---

## 👥 Project Team

**Developer**: Shelly Chang  
**Supervision**: AlbertSchool M2-1  
**Date**: November 1, 2025  

---

## 💡 Conclusion

This project demonstrates the complete MLOps lifecycle:

1. **Data Engineering** → Automated data processing
2. **Model Development** → CNN training and optimization
3. **Experiment Management** → MLflow tracking
4. **Model Deployment** → FastAPI service
5. **User Interface** → React Web App
6. **Containerization** → Docker deployment

Through this project, we successfully achieved:
- ✅ Complete pipeline from data to deployment
- ✅ Reproducible experimental environment
- ✅ Production-grade code quality
- ✅ User-friendly interface

**This is a production-ready MLOps project example!**

---

## 🙏 Acknowledgments

Thanks to AlbertSchool for providing the learning opportunity and guidance!

---

**End of Presentation**

Questions welcome! 🚀

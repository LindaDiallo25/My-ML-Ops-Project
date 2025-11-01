# 🚀 Quick Start Guide

## Current Status

✅ All core files are ready!

## 📍 Important Paths

Your project is located at:
```
/Users/shellychang/Library/CloudStorage/GoogleDrive-shuhc121@gmail.com/我的雲端硬碟/Albertschool_M2_1/as_m2-1/ML Ops/MLOP_project/ML-Ops-project
```

## 🎯 Start Services (3 Steps)

### Method 1: Using Startup Scripts (Recommended)

#### Step 1: Start the API

Open terminal and run:

```bash
cd "/Users/shellychang/Library/CloudStorage/GoogleDrive-shuhc121@gmail.com/我的雲端硬碟/Albertschool_M2_1/as_m2-1/ML Ops/MLOP_project/ML-Ops-project"

./start_api.sh
```

You should see:
```
🚀 Starting MLOps API Server...
✅ Model file found
✅ Dependencies ready
🌐 Starting FastAPI server on http://localhost:8000
📚 API docs will be available at http://localhost:8000/docs
```

**Keep this terminal running!**

#### Step 2: Start Frontend (New Terminal)

Open a **new** terminal window and run:

```bash
cd "/Users/shellychang/Library/CloudStorage/GoogleDrive-shuhc121@gmail.com/我的雲端硬碟/Albertschool_M2_1/as_m2-1/ML Ops/MLOP_project/ML-Ops-project"

./start_frontend.sh
```

The frontend will automatically install dependencies and start.

#### Step 3: Access the Application

Open your browser:
- **前端 WebApp**: http://localhost:5173
- **API 文檔**: http://localhost:8000/docs
- **API 健康檢查**: http://localhost:8000/health

---

### Method 2: Manual Startup

#### Terminal 1 - Start API

```bash
cd "/Users/shellychang/Library/CloudStorage/GoogleDrive-shuhc121@gmail.com/我的雲端硬碟/Albertschool_M2_1/as_m2-1/ML Ops/MLOP_project/ML-Ops-project/api"

python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### Terminal 2 - Start Frontend

```bash
cd "/Users/shellychang/Library/CloudStorage/GoogleDrive-shuhc121@gmail.com/我的雲端硬碟/Albertschool_M2_1/as_m2-1/ML Ops/MLOP_project/ML-Ops-project/Front"

npm install
npm run dev
```

---

## 🧪 Test the API

### Testing with curl

```bash
# Health check
curl http://localhost:8000/health

# Test prediction (using sample image)
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@cleaned_images_for_model/dandelion_00000000.jpg"
```

### Using Swagger UI

Open browser and visit: http://localhost:8000/docs

Click the `/predict` endpoint and upload an image to test.

---

## 🎨 Using the WebApp

1. Open http://localhost:5173
2. Click or drag & drop an image to the upload area
3. Wait for classification results (2-3 seconds)
4. View the predicted class and confidence score
5. Click "Reclassify" or "Upload Another"

---

## ❌ Troubleshooting

### Issue 1: Port 8000 already in use

```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9

# Restart API
./start_api.sh
```

### Issue 2: Model file not found

Ensure `dandelion_grass_cnn.keras` is in the project root:

```bash
ls -lh dandelion_grass_cnn.keras
```

If not found, retrain the model:

```bash
python3 train_with_mlflow.py
```

### Issue 3: Frontend cannot connect to API

Check:
1. API is running on http://localhost:8000
2. No CORS errors in browser console
3. Verify API URL in `Front/src/App.tsx`

### Issue 4: npm install fails

```bash
cd Front
rm -rf node_modules package-lock.json
npm install
```

---

## 🐳 Using Docker Compose (Advanced)

If you have Docker Desktop installed:

```bash
cd "/Users/shellychang/Library/CloudStorage/GoogleDrive-shuhc121@gmail.com/我的雲端硬碟/Albertschool_M2_1/as_m2-1/ML Ops/MLOP_project/ML-Ops-project"

docker-compose up --build
```

Services:
- 前端: http://localhost:3000
- API: http://localhost:8000
- MLflow: http://localhost:5000
- Minio: http://localhost:9001

---

## 📝 Quick Checklist

- [ ] API running on http://localhost:8000
- [ ] Visit http://localhost:8000/docs to see Swagger UI
- [ ] Frontend running on http://localhost:5173
- [ ] Can upload images and see prediction results
- [ ] Prediction shows "dandelion" or "grass"
- [ ] Confidence displayed as percentage

---

## 🎉 After Successful Launch

Congratulations! Your MLOps project is fully operational.

**Next Steps:**
1. Test with different images
2. Check MLflow UI (if running): http://localhost:5000
3. Prepare demo video recording
4. Prepare project documentation for submission

---

**Need help?** Check `README.md` and `QUICKSTART.md` for more details.

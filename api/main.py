"""
FastAPI application for plant classification (Dandelion versus Grass).
Provides endpoints for image prediction and health checks.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
import tensorflow as tf
from io import BytesIO
import logging
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Plant Classification API",
    description="Binary classifier for Dandelion vs Grass images",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
model = None
IMAGE_SIZE = (256, 256)
CLASS_NAMES = ["dandelion", "grass"]

def load_model_from_mlflow():
    """Load model from MLflow Model Registry (online)."""
    global model
    try:
        import mlflow
        import mlflow.pyfunc
        
        # Configuration MLflow
        mlflow.set_tracking_uri("http://mlflow:5000")
        
        # Try to get the latest version
        client = mlflow.tracking.MlflowClient()
        
        # First, try to get Production version
        try:
            versions = client.get_latest_versions("dandelion-grass-classifier", stages=["Production"])
            if versions:
                model_version = versions[0].version
                logger.info(f"📥 Loading model version {model_version} from Production stage")
            else:
                raise Exception("No Production version found")
        except:
            # If no Production version, get latest version
            versions = client.get_latest_versions("dandelion-grass-classifier")
            if not versions:
                raise Exception("No model versions found")
            model_version = versions[0].version
            logger.info(f"📥 Loading latest model version {model_version}")
        
        # Load model directly with keras flavor
        model_uri = f"models:/dandelion-grass-classifier/{model_version}"
        import mlflow.keras
        model = mlflow.keras.load_model(model_uri)
        
        logger.info(f"✅ Model loaded successfully from MLflow Model Registry (version {model_version})")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error loading model from MLflow: {e}")
        logger.info("⚠️  Falling back to local file...")
        return load_model_from_file()


def load_model_from_file():
    """Load the trained Keras model from local file (fallback)."""
    global model
    try:
        # Try /app/models first (Docker container path)
        model_path = Path("/app/models/dandelion_grass_cnn.keras")
        if not model_path.exists():
            # Try models directory (local development)
            model_path = Path("../models/dandelion_grass_cnn.keras")
            if not model_path.exists():
                # Fallback to old location
                model_path = Path("dandelion_grass_cnn.keras")
                if not model_path.exists():
                    model_path = Path("../dandelion_grass_cnn.keras")
        
        if model_path.exists():
            model = tf.keras.models.load_model(str(model_path))
            logger.info(f"✅ Model loaded successfully from local file: {model_path}")
            return True
        else:
            logger.error(f"❌ Model file not found at {model_path}")
            return False
    except Exception as e:
        logger.error(f"❌ Error loading model: {e}")
        return False

@app.on_event("startup")
async def startup_event():
    """Load model on startup."""
    logger.info("🚀 Starting up API...")
    
    # Try loading from MLflow first (online), fallback to local file
    success = load_model_from_mlflow()
    
    if not success:
        logger.warning("⚠️  Model not loaded. Predictions will fail until model is available.")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Plant Classification API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "/predict": "POST - Upload image for classification",
            "/health": "GET - Health check",
            "/docs": "GET - API documentation"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    model_loaded = model is not None
    return {
        "status": "healthy" if model_loaded else "degraded",
        "model_loaded": model_loaded,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict plant class from uploaded image.
    
    Args:
        file: Image file (JPG, PNG)
    
    Returns:
        JSON with prediction, confidence, and class probabilities
    """
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please ensure the model file exists."
        )
    
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="File must be an image (JPG, PNG, etc.)"
        )
    
    try:
        # Read and preprocess image
        image_data = await file.read()
        image = Image.open(BytesIO(image_data))
        
        # Convert to RGB (remove alpha channel if present)
        image = image.convert("RGB")
        
        # Resize to model input size
        image = image.resize(IMAGE_SIZE)
        
        # Convert to array and normalize
        img_array = np.asarray(image) / 255.0
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        
        # Make prediction
        prediction = model.predict(img_array, verbose=0)
        
        # For binary classification with sigmoid
        if prediction.shape[-1] == 1:
            confidence = float(prediction[0][0])
            predicted_class = CLASS_NAMES[1] if confidence > 0.5 else CLASS_NAMES[0]
            
            result = {
                "predicted_class": predicted_class,
                "confidence": confidence if confidence > 0.5 else 1 - confidence,
                "probabilities": {
                    CLASS_NAMES[0]: float(1 - confidence),
                    CLASS_NAMES[1]: float(confidence)
                },
                "timestamp": datetime.now().isoformat()
            }
        else:
            # Multi-class with softmax
            predicted_idx = int(np.argmax(prediction[0]))
            predicted_class = CLASS_NAMES[predicted_idx]
            confidence = float(prediction[0][predicted_idx])
            
            result = {
                "predicted_class": predicted_class,
                "confidence": confidence,
                "probabilities": {
                    CLASS_NAMES[i]: float(prediction[0][i]) 
                    for i in range(len(CLASS_NAMES))
                },
                "timestamp": datetime.now().isoformat()
            }
        
        logger.info(f"Prediction: {predicted_class} ({confidence:.2%})")
        return result
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )

@app.get("/model-info")
async def model_info():
    """Get information about the loaded model."""
    if model is None:
        return {"error": "Model not loaded"}
    
    return {
        "model_type": "CNN (Convolutional Neural Network)",
        "input_shape": list(model.input_shape),
        "output_shape": list(model.output_shape),
        "classes": CLASS_NAMES,
        "image_size": IMAGE_SIZE,
        "total_params": model.count_params()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

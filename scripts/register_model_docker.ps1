# Script PowerShell pour enregistrer le modèle dans MLflow depuis Docker
# Usage: .\scripts\register_model_docker.ps1

Write-Host "🚀 Registering model in MLflow Model Registry from Docker..." -ForegroundColor Cyan

$pythonScript = @'
import mlflow
import mlflow.keras
import tensorflow as tf
from pathlib import Path

# Set MLflow tracking URI
mlflow.set_tracking_uri("http://mlflow:5000")

# Set experiment
mlflow.set_experiment("dandelion_grass_classification")

model_path = Path("/app/models/dandelion_grass_cnn.keras")
model_name = "dandelion-grass-classifier"

if not model_path.exists():
    print(f"❌ Model file not found: {model_path}")
    exit(1)

print(f"📦 Loading model from: {model_path}")
model = tf.keras.models.load_model(str(model_path))
print(f"✅ Model loaded successfully")

# Start a new run to register the model
with mlflow.start_run(run_name="model_registration_from_docker") as run:
    
    # Log model information
    mlflow.log_param("model_path", str(model_path))
    mlflow.log_param("model_type", "CNN")
    mlflow.log_param("input_shape", str(model.input_shape))
    mlflow.log_param("total_params", model.count_params())
    
    # Log the model with automatic registration
    print(f"📤 Logging and registering model in MLflow...")
    mlflow.keras.log_model(
        model, 
        "model",
        registered_model_name=model_name
    )
    
    print(f"\n✅ Model registered successfully!")
    print(f"   Model name: {model_name}")
    print(f"   Run ID: {run.info.run_id}")
    print(f"\n📊 View in MLflow UI: http://localhost:5000/#/models/{model_name}")
'@

# Exécuter le script Python dans le conteneur Docker
docker exec -i mlops_api python3 -c $pythonScript

Write-Host ""
Write-Host "✅ Done! Check MLflow UI: http://localhost:5000/#/models" -ForegroundColor Green


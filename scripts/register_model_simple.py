"""
Simple script to register model in MLflow - designed to run inside Docker container.
Run with: docker exec mlops_api python3 /app/api/../scripts/register_model_simple.py
"""

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

print("="*60)
print("MLflow Model Registration")
print("="*60)

if not model_path.exists():
    print(f"ERROR: Model file not found: {model_path}")
    exit(1)

print(f"\n[1/3] Loading model from: {model_path}")
model = tf.keras.models.load_model(str(model_path))
print(f"      SUCCESS - Model loaded")
print(f"      Input shape: {model.input_shape}")
print(f"      Output shape: {model.output_shape}")
print(f"      Total parameters: {model.count_params():,}")

# Start a new run to register the model
print(f"\n[2/3] Creating MLflow run...")
with mlflow.start_run(run_name="model_registration") as run:
    
    # Log model information
    mlflow.log_param("model_path", str(model_path))
    mlflow.log_param("model_type", "CNN")
    mlflow.log_param("input_shape", str(model.input_shape))
    mlflow.log_param("output_shape", str(model.output_shape))
    mlflow.log_param("total_params", model.count_params())
    
    # Log the model with automatic registration
    print(f"\n[3/3] Registering model in MLflow Model Registry...")
    print(f"      Model name: {model_name}")
    
    result = mlflow.keras.log_model(
        model, 
        "model",
        registered_model_name=model_name
    )
    
    print(f"\n" + "="*60)
    print("SUCCESS - Model registered!")
    print("="*60)
    print(f"Model name: {model_name}")
    print(f"Run ID: {run.info.run_id}")
    print(f"\nView in MLflow UI:")
    print(f"  - All models: http://localhost:5000/#/models")
    print(f"  - This model: http://localhost:5000/#/models/{model_name}")
    print("="*60)


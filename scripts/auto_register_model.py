#!/usr/bin/env python3
"""
Auto-register model in MLflow Model Registry on startup.
This script runs automatically when Docker containers start.
"""

import mlflow
import mlflow.keras
import tensorflow as tf
from pathlib import Path
import time
import sys


def wait_for_mlflow(max_retries=30, delay=2):
    """Wait for MLflow server to be ready."""
    print("Waiting for MLflow server to be ready...")
    
    for i in range(max_retries):
        try:
            client = mlflow.tracking.MlflowClient()
            client.search_experiments()
            print("MLflow server is ready!")
            return True
        except Exception as e:
            print(f"Attempt {i+1}/{max_retries}: MLflow not ready yet... ({e})")
            time.sleep(delay)
    
    print("ERROR: MLflow server did not become ready in time")
    return False


def check_model_exists(model_name):
    """Check if model is already registered."""
    try:
        client = mlflow.tracking.MlflowClient()
        client.get_registered_model(model_name)
        return True
    except Exception:
        return False


def register_model(model_path, model_name="dandelion-grass-classifier"):
    """Register model in MLflow Model Registry."""
    
    print("="*70)
    print("MLflow Model Auto-Registration")
    print("="*70)
    
    # Check if model already exists
    if check_model_exists(model_name):
        print(f"\n✓ Model '{model_name}' is already registered in MLflow")
        print(f"  View at: http://localhost:5000/#/models/{model_name}")
        print("="*70)
        return True
    
    print(f"\nModel '{model_name}' not found. Registering now...")
    
    # Check if model file exists
    model_path = Path(model_path)
    if not model_path.exists():
        print(f"ERROR: Model file not found at {model_path}")
        return False
    
    try:
        # Load model
        print(f"\n[1/3] Loading model from: {model_path}")
        model = tf.keras.models.load_model(str(model_path))
        print(f"      ✓ Model loaded successfully")
        print(f"      - Input shape: {model.input_shape}")
        print(f"      - Output shape: {model.output_shape}")
        print(f"      - Total parameters: {model.count_params():,}")
        
        # Set experiment
        mlflow.set_experiment("dandelion_grass_classification")
        
        # Create run and register model
        print(f"\n[2/3] Creating MLflow run...")
        with mlflow.start_run(run_name="auto_model_registration") as run:
            
            # Log parameters
            mlflow.log_param("model_path", str(model_path))
            mlflow.log_param("model_type", "CNN")
            mlflow.log_param("input_shape", str(model.input_shape))
            mlflow.log_param("output_shape", str(model.output_shape))
            mlflow.log_param("total_params", model.count_params())
            mlflow.log_param("classes", "dandelion, grass")
            mlflow.log_param("auto_registered", "true")
            
            # Log and register model with proper artifact path
            print(f"\n[3/3] Registering model in Model Registry...")
            
            # Create a signature for the model
            import numpy as np
            from mlflow.models.signature import infer_signature
            
            # Create sample input
            sample_input = np.random.rand(1, 256, 256, 3).astype(np.float32)
            sample_output = model.predict(sample_input, verbose=0)
            signature = infer_signature(sample_input, sample_output)
            
            # Log model with signature
            mlflow.keras.log_model(
                model,
                "model",
                registered_model_name=model_name,
                signature=signature
            )
            
            print(f"\n{'='*70}")
            print("SUCCESS - Model registered in MLflow!")
            print("="*70)
            print(f"Model name: {model_name}")
            print(f"Version: 1")
            print(f"Run ID: {run.info.run_id}")
            print(f"\nView in MLflow UI:")
            print(f"  http://localhost:5000/#/models/{model_name}")
            print("="*70)
            
        return True
        
    except Exception as e:
        print(f"\nERROR: Failed to register model")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Set MLflow tracking URI
    mlflow.set_tracking_uri("http://mlflow:5000")
    
    # Wait for MLflow to be ready
    if not wait_for_mlflow():
        print("Skipping model registration - MLflow not available")
        sys.exit(1)
    
    # Register model
    model_path = "/app/models/dandelion_grass_cnn.keras"
    success = register_model(model_path)
    
    if success:
        print("\n✓ Auto-registration completed successfully")
        sys.exit(0)
    else:
        print("\n✗ Auto-registration failed")
        sys.exit(1)


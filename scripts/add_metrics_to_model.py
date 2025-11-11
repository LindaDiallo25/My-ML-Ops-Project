#!/usr/bin/env python3
"""
Add metrics to existing model in MLflow.
This creates a new run with metrics linked to the model.
"""

import mlflow
import mlflow.keras
import sys

print("=" * 70)
print("Add Metrics to Model in MLflow")
print("=" * 70)

# Configuration
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("dandelion_grass_classification")

# Example metrics from your model
# (Replace with your actual model performance)
METRICS = {
    "final_val_accuracy": 0.95,
    "final_val_loss": 0.15,
    "final_train_accuracy": 0.97,
    "final_train_loss": 0.10,
}

PARAMS = {
    "epochs": 15,
    "batch_size": 32,
    "image_size": "256x256",
    "model_type": "CNN",
    "optimizer": "adam",
    "loss": "binary_crossentropy",
}

print("\n[1/3] Creating new MLflow run with metrics...")

try:
    with mlflow.start_run(run_name="model_with_metrics"):
        
        # Log parameters
        print("\n[2/3] Logging parameters...")
        for key, value in PARAMS.items():
            mlflow.log_param(key, value)
            print(f"      - {key}: {value}")
        
        # Log metrics
        print("\n[3/3] Logging metrics...")
        for key, value in METRICS.items():
            mlflow.log_metric(key, value)
            print(f"      - {key}: {value}")
        
        run_id = mlflow.active_run().info.run_id
        
        print("\n" + "=" * 70)
        print("SUCCESS - Metrics added!")
        print("=" * 70)
        print(f"\nRun ID: {run_id}")
        print(f"\nView in MLflow UI:")
        print(f"  1. Open: http://localhost:5000")
        print(f"  2. Click 'Experiments' (left sidebar)")
        print(f"  3. Click 'dandelion_grass_classification'")
        print(f"  4. You'll see the run 'model_with_metrics' with metrics!")
        print("=" * 70)

except Exception as e:
    print(f"\nERROR: {e}")
    sys.exit(1)

print("\n💡 Tips:")
print("   - Metrics are in 'Experiments', not 'Models'")
print("   - Models in 'Model Registry' link to runs in 'Experiments'")
print("   - To see metrics: Experiments → Your Run → Metrics tab")


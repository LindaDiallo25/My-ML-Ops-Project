#!/usr/bin/env python3
"""
Register an existing trained model in MLflow Model Registry.
This script can register a model from an existing MLflow run or a local file.
"""

import mlflow
import mlflow.keras
import tensorflow as tf
from pathlib import Path
import sys


def register_from_run(run_id: str, model_name: str = "dandelion-grass-classifier"):
    """
    Register a model from an existing MLflow run.
    
    Args:
        run_id: The MLflow run ID containing the model
        model_name: Name for the registered model
    """
    try:
        model_uri = f"runs:/{run_id}/model"
        
        print(f"🔍 Searching for model in run: {run_id}")
        model_version = mlflow.register_model(model_uri, model_name)
        
        print(f"\n✅ Model registered successfully!")
        print(f"   Model name: {model_name}")
        print(f"   Version: {model_version.version}")
        print(f"\n📊 View in MLflow UI: http://localhost:5000/#/models/{model_name}")
        
        return model_version
        
    except Exception as e:
        print(f"❌ Error registering model: {e}")
        sys.exit(1)


def register_from_local_file(
    model_path: str, 
    model_name: str = "dandelion-grass-classifier",
    description: str = "Dandelion vs Grass CNN Classifier"
):
    """
    Register a model from a local file by creating a new MLflow run.
    
    Args:
        model_path: Path to the .keras model file
        model_name: Name for the registered model
        description: Description of the model
    """
    try:
        model_path = Path(model_path)
        
        if not model_path.exists():
            print(f"❌ Model file not found: {model_path}")
            sys.exit(1)
        
        print(f"📦 Loading model from: {model_path}")
        model = tf.keras.models.load_model(str(model_path))
        print(f"✅ Model loaded successfully")
        
        # Set experiment
        mlflow.set_experiment("dandelion_grass_classification")
        
        # Start a new run to register the model
        with mlflow.start_run(run_name="model_registration") as run:
            
            # Log model information
            mlflow.log_param("model_path", str(model_path))
            mlflow.log_param("model_type", "CNN")
            mlflow.log_param("input_shape", str(model.input_shape))
            mlflow.log_param("total_params", model.count_params())
            
            # Log the model
            print(f"📤 Logging model to MLflow...")
            mlflow.keras.log_model(
                model, 
                "model",
                registered_model_name=model_name
            )
            
            print(f"\n✅ Model registered successfully!")
            print(f"   Model name: {model_name}")
            print(f"   Run ID: {run.info.run_id}")
            print(f"\n📊 View in MLflow UI: http://localhost:5000/#/models/{model_name}")
            
    except Exception as e:
        print(f"❌ Error registering model: {e}")
        sys.exit(1)


def list_recent_runs(experiment_name: str = "dandelion_grass_classification", limit: int = 5):
    """List recent MLflow runs to help find run IDs."""
    try:
        client = mlflow.tracking.MlflowClient()
        experiment = client.get_experiment_by_name(experiment_name)
        
        if not experiment:
            print(f"❌ Experiment '{experiment_name}' not found")
            return
        
        runs = client.search_runs(
            experiment_ids=[experiment.experiment_id],
            order_by=["start_time DESC"],
            max_results=limit
        )
        
        if not runs:
            print(f"⚠️  No runs found in experiment '{experiment_name}'")
            return
        
        print(f"\n📋 Recent runs in '{experiment_name}':\n")
        print(f"{'Run ID':<35} {'Run Name':<30} {'Accuracy':<10}")
        print("-" * 80)
        
        for run in runs:
            run_id = run.info.run_id
            run_name = run.data.tags.get("mlflow.runName", "N/A")
            accuracy = run.data.metrics.get("final_val_accuracy", None)
            accuracy_str = f"{accuracy:.4f}" if accuracy else "N/A"
            
            print(f"{run_id:<35} {run_name:<30} {accuracy_str:<10}")
        
        print()
        
    except Exception as e:
        print(f"❌ Error listing runs: {e}")


if __name__ == "__main__":
    import argparse
    
    # Set MLflow tracking URI
    mlflow.set_tracking_uri("http://localhost:5000")
    
    parser = argparse.ArgumentParser(
        description="Register a model in MLflow Model Registry"
    )
    parser.add_argument(
        "--mode",
        choices=["run", "file", "list"],
        default="file",
        help="Registration mode: 'run' (from MLflow run), 'file' (from local file), or 'list' (list recent runs)"
    )
    parser.add_argument(
        "--run-id",
        help="MLflow run ID (required for 'run' mode)"
    )
    parser.add_argument(
        "--model-path",
        default="../models/dandelion_grass_cnn.keras",
        help="Path to model file (for 'file' mode, default: ../models/dandelion_grass_cnn.keras)"
    )
    parser.add_argument(
        "--model-name",
        default="dandelion-grass-classifier",
        help="Name for the registered model (default: dandelion-grass-classifier)"
    )
    
    args = parser.parse_args()
    
    if args.mode == "list":
        list_recent_runs()
        
    elif args.mode == "run":
        if not args.run_id:
            print("❌ Error: --run-id is required for 'run' mode")
            print("   Use --mode list to see available run IDs")
            sys.exit(1)
        register_from_run(args.run_id, args.model_name)
        
    elif args.mode == "file":
        register_from_local_file(args.model_path, args.model_name)
    
    print("\n💡 Tips:")
    print("   - View models: http://localhost:5000/#/models")
    print("   - Transition model stages: Production, Staging, Archived")
    print("   - Load model: mlflow.keras.load_model(f'models:/{args.model_name}/1')")


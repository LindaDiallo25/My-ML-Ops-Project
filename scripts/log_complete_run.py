#!/usr/bin/env python3
"""
Log a complete run with all model parameters and metrics to MLflow.
Template for tracking model information.
"""

import mlflow
import sys

def log_complete_model_info(
    # Training params
    epochs=15,
    batch_size=32,
    image_size="256x256",
    optimizer="adam",
    loss_function="binary_crossentropy",
    # Model params
    model_path="/app/models/dandelion_grass_cnn.keras",
    model_type="CNN",
    input_shape="(None, 256, 256, 3)",
    output_shape="(None, 1)",
    total_params=14839105,
    classes="dandelion, grass",
    num_classes=2,
    # Data params
    train_test_split=0.8,
    random_seed=42,
    # Metrics
    val_accuracy=0.95,
    val_loss=0.15,
    train_accuracy=0.97,
    train_loss=0.10,
    precision=0.94,
    recall=0.96,
    f1_score=0.95,
    # Run name
    run_name="complete_model_info"
):
    """
    Log complete model information to MLflow.
    
    Args:
        Training, model, data parameters and metrics
        
    Returns:
        run_id: MLflow run ID
    """
    
    print("=" * 70)
    print("Logging Complete Model Info to MLflow")
    print("=" * 70)
    
    mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_experiment("dandelion_grass_classification")
    
    try:
        with mlflow.start_run(run_name=run_name):
            
            # Log training parameters
            print("\n[1/4] Logging training parameters...")
            mlflow.log_param("epochs", epochs)
            mlflow.log_param("batch_size", batch_size)
            mlflow.log_param("image_size", image_size)
            mlflow.log_param("optimizer", optimizer)
            mlflow.log_param("loss", loss_function)
            
            # Log model architecture
            print("[2/4] Logging model architecture...")
            mlflow.log_param("model_path", model_path)
            mlflow.log_param("model_type", model_type)
            mlflow.log_param("input_shape", input_shape)
            mlflow.log_param("output_shape", output_shape)
            mlflow.log_param("total_params", total_params)
            mlflow.log_param("classes", classes)
            mlflow.log_param("num_classes", num_classes)
            
            # Log data configuration
            print("[3/4] Logging data configuration...")
            mlflow.log_param("train_test_split", train_test_split)
            mlflow.log_param("random_seed", random_seed)
            
            # Log metrics
            print("[4/4] Logging performance metrics...")
            mlflow.log_metric("final_val_accuracy", val_accuracy)
            mlflow.log_metric("final_val_loss", val_loss)
            mlflow.log_metric("final_train_accuracy", train_accuracy)
            mlflow.log_metric("final_train_loss", train_loss)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("recall", recall)
            mlflow.log_metric("f1_score", f1_score)
            
            run_id = mlflow.active_run().info.run_id
            
            print("\n" + "=" * 70)
            print("SUCCESS!")
            print("=" * 70)
            print(f"\nRun ID: {run_id}")
            print(f"Run Name: {run_name}")
            print(f"\nView in MLflow UI:")
            print(f"  http://localhost:5000/#/experiments/1/runs/{run_id}")
            print("=" * 70)
            
            return run_id
            
    except Exception as e:
        print(f"\nERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Example: Log with default values
    run_id = log_complete_model_info()
    
    print("\n💡 Usage:")
    print("   - View: http://localhost:5000")
    print("   - Navigate: Experiments → dandelion_grass_classification")
    print("   - Click on your run to see all parameters and metrics!")


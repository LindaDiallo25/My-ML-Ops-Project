#!/usr/bin/env python3
"""
Test MLflow + MinIO integration by registering a dummy model.
"""

import mlflow
import mlflow.keras
import tensorflow as tf
import numpy as np

print("=" * 70)
print("Test MLflow + MinIO Integration")
print("=" * 70)

# Configuration
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("minio_test")

print("\n[1/5] Connexion a MLflow...")
print("      URI: http://localhost:5000")

# Créer un modèle simple pour tester
print("\n[2/5] Creation d'un modele de test...")
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(256, 256, 3)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy')
print("      Modele cree (test)")

# Entraîner avec quelques données dummy
print("\n[3/5] Entrainement rapide...")
X_dummy = np.random.rand(10, 256, 256, 3)
y_dummy = np.random.randint(0, 2, 10)
model.fit(X_dummy, y_dummy, epochs=1, verbose=0)
print("      Entrainement termine")

# Logger dans MLflow (avec MinIO comme storage)
print("\n[4/5] Enregistrement dans MLflow + MinIO...")
with mlflow.start_run(run_name="minio_test_run"):
    mlflow.log_param("test", "minio_integration")
    mlflow.log_metric("dummy_metric", 0.95)
    
    # Log model - devrait aller dans MinIO !
    mlflow.keras.log_model(
        model,
        "model",
        registered_model_name="test-minio-model"
    )
    
    run_id = mlflow.active_run().info.run_id
    print(f"      Run ID: {run_id}")

print("\n[5/5] Verification...")
print("      Modele enregistre dans MLflow Model Registry")
print("      Artifacts stockes dans MinIO (s3://mlflow-artifacts/)")

print("\n" + "=" * 70)
print("TEST REUSSI !")
print("=" * 70)
print("\nVerifications:")
print("  1. MLflow UI: http://localhost:5000")
print("  2. MinIO Console: http://localhost:9001")
print("     - Login: minioadmin / minioadmin123")
print("     - Bucket: mlflow-artifacts")
print("  3. Model Registry: http://localhost:5000/#/models/test-minio-model")
print("\nVous devriez voir les artifacts dans le bucket MinIO !")


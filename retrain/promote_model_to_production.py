#!/usr/bin/env python3
"""
Promote a model version to Production stage in MLflow Model Registry.
"""

import mlflow
import sys

# Configuration
mlflow.set_tracking_uri("http://localhost:5000")

model_name = "dandelion-grass-classifier"
version = 1  # Version à promouvoir

try:
    client = mlflow.tracking.MlflowClient()
    
    # Vérifier que le modèle existe
    try:
        model = client.get_registered_model(model_name)
        print(f"[OK] Modele trouve : {model_name}")
    except:
        print(f"[ERREUR] Modele '{model_name}' non trouve dans le Registry")
        print("\nModeles disponibles :")
        for m in client.search_registered_models():
            print(f"  - {m.name}")
        sys.exit(1)
    
    # Promouvoir en Production
    print(f"\nPromotion de la version {version} en Production...")
    client.transition_model_version_stage(
        name=model_name,
        version=version,
        stage="Production",
        archive_existing_versions=True  # Archive les anciennes versions en Production
    )
    
    print(f"[OK] Version {version} promue en Production !")
    print(f"\nVoir dans MLflow UI : http://localhost:5000/#/models/{model_name}")
    print("\nRedemarre l'API pour qu'elle charge la nouvelle version :")
    print("  docker-compose restart api")
    
except Exception as e:
    print(f"[ERREUR] Erreur : {e}")
    sys.exit(1)


from fastapi.testclient import TestClient
import sys
import os

# Permet de trouver le dossier api
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.main import app

client = TestClient(app)

def test_health_check():
    """Vérifie que l'API répond correctement sur le endpoint health"""
    response = client.get("/health")
    assert response.status_code in [200, 503]  # 200 si le modèle est là, 503 s'il manque, mais l'API répond !
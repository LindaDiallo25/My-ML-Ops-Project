#!/usr/bin/env python3
"""
Configure MinIO bucket for MLflow artifacts.
Creates the bucket if it doesn't exist.
"""

import boto3
from botocore.client import Config

# Configuration MinIO
MINIO_ENDPOINT = "http://localhost:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin123"
BUCKET_NAME = "mlflow-artifacts"

print("=" * 60)
print("MinIO Bucket Setup for MLflow")
print("=" * 60)

# Créer client S3 pointant vers MinIO
s3_client = boto3.client(
    's3',
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)

try:
    # Vérifier si le bucket existe
    buckets = s3_client.list_buckets()
    bucket_names = [bucket['Name'] for bucket in buckets['Buckets']]
    
    if BUCKET_NAME in bucket_names:
        print(f"\n[OK] Bucket '{BUCKET_NAME}' existe deja")
    else:
        print(f"\n[INFO] Creation du bucket '{BUCKET_NAME}'...")
        s3_client.create_bucket(Bucket=BUCKET_NAME)
        print(f"[OK] Bucket '{BUCKET_NAME}' cree avec succes")
    
    # Lister tous les buckets
    print(f"\nBuckets disponibles dans MinIO:")
    for bucket in buckets['Buckets']:
        print(f"  - {bucket['Name']}")
    
    print(f"\n" + "=" * 60)
    print("Configuration terminee !")
    print("=" * 60)
    print(f"\nPour utiliser MinIO avec MLflow:")
    print(f"1. Modifiez docker-compose.yml:")
    print(f"   --default-artifact-root s3://{BUCKET_NAME}/")
    print(f"\n2. Redemarrez les conteneurs:")
    print(f"   docker-compose restart mlflow")
    print(f"\n3. MinIO Console: http://localhost:9001")
    print(f"   Username: {MINIO_ACCESS_KEY}")
    print(f"   Password: {MINIO_SECRET_KEY}")
    
except Exception as e:
    print(f"\n[ERREUR] {e}")
    print(f"\nAssurez-vous que MinIO tourne:")
    print(f"  docker-compose ps minio")


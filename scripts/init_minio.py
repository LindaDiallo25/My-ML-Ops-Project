#!/usr/bin/env python3
"""
Initialize MinIO bucket for MLflow artifacts.
Runs automatically on API container startup.
"""

import boto3
from botocore.client import Config
import time
import sys

MINIO_ENDPOINT = "http://minio:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin123"
BUCKET_NAME = "mlflow-artifacts"

def wait_for_minio(max_retries=30, delay=2):
    """Wait for MinIO to be ready."""
    print("Waiting for MinIO server to be ready...")
    
    for i in range(max_retries):
        try:
            s3_client = boto3.client(
                's3',
                endpoint_url=MINIO_ENDPOINT,
                aws_access_key_id=MINIO_ACCESS_KEY,
                aws_secret_access_key=MINIO_SECRET_KEY,
                config=Config(signature_version='s3v4')
            )
            s3_client.list_buckets()
            print("MinIO server is ready!")
            return s3_client
        except Exception as e:
            print(f"Attempt {i+1}/{max_retries}: MinIO not ready yet...")
            time.sleep(delay)
    
    print("ERROR: MinIO server did not become ready in time")
    return None

def create_bucket_if_not_exists(s3_client):
    """Create bucket if it doesn't exist."""
    try:
        buckets = s3_client.list_buckets()
        bucket_names = [bucket['Name'] for bucket in buckets['Buckets']]
        
        if BUCKET_NAME in bucket_names:
            print(f"✓ Bucket '{BUCKET_NAME}' already exists")
            return True
        else:
            print(f"Creating bucket '{BUCKET_NAME}'...")
            s3_client.create_bucket(Bucket=BUCKET_NAME)
            print(f"✓ Bucket '{BUCKET_NAME}' created successfully")
            return True
            
    except Exception as e:
        print(f"ERROR creating bucket: {e}")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("MinIO Initialization")
    print("=" * 70)
    
    s3_client = wait_for_minio()
    
    if s3_client:
        success = create_bucket_if_not_exists(s3_client)
        if success:
            print("=" * 70)
            print("MinIO ready for MLflow!")
            print("=" * 70)
            sys.exit(0)
    
    print("MinIO initialization failed, continuing anyway...")
    sys.exit(0)  # Don't fail the container startup


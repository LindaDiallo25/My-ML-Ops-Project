#!/usr/bin/env python3
"""
Quick test script to verify API functionality.
"""

import requests
from pathlib import Path
import sys

def test_api_health():
    """Test API health endpoint."""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Is it running on port 8000?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_prediction(image_path):
    """Test prediction endpoint with an image."""
    if not Path(image_path).exists():
        print(f"❌ Image not found: {image_path}")
        return False
    
    try:
        with open(image_path, "rb") as f:
            files = {"file": (Path(image_path).name, f, "image/jpeg")}
            response = requests.post(
                "http://localhost:8000/predict",
                files=files,
                timeout=10
            )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Prediction successful!")
            print(f"   Class: {data['predicted_class']}")
            print(f"   Confidence: {data['confidence']:.2%}")
            print(f"   Probabilities: {data['probabilities']}")
            return True
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Testing API Endpoints")
    print("=" * 60)
    
    # Test health
    print("\n1. Testing health endpoint...")
    test_api_health()
    
    # Test prediction with sample image
    print("\n2. Testing prediction endpoint...")
    sample_image = Path("cleaned_images_for_model/dandelion_00000000.jpg")
    if sample_image.exists():
        test_prediction(str(sample_image))
    else:
        print("⚠️  No sample image found for testing")
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)

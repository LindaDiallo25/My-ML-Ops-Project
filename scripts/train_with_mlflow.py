#!/usr/bin/env python3
"""
Train CNN model with MLflow tracking.
Integrates model training with experiment tracking and S3 storage.
"""

import os
import sys
import numpy as np
from PIL import Image, UnidentifiedImageError
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import mlflow
import mlflow.keras
from datetime import datetime


def load_data(image_dir, image_size):
    """Loads all cleaned images from the directory and extracts labels from filenames."""
    print(f"Loading images from: {image_dir}")
    images = []
    labels = []
    
    if not os.path.exists(image_dir):
        print(f"Error: Directory not found: '{image_dir}'", file=sys.stderr)
        sys.exit(1)
        
    for filename in os.listdir(image_dir):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
            
        try:
            label = filename.split('_')[0]
        except IndexError:
            print(f"Warning: Skipping file with unusual name: {filename}")
            continue
            
        try:
            img_path = os.path.join(image_dir, filename)
            with Image.open(img_path) as img:
                if img.size != image_size:
                    img = img.resize(image_size)
                
                img_array = np.asarray(img) / 255.0
                images.append(img_array)
                labels.append(label)
                
        except (IOError, UnidentifiedImageError, OSError) as e:
            print(f"Warning: Skipping corrupt image {filename}: {e}")
            
    if not images:
        print("Error: No images were successfully loaded.", file=sys.stderr)
        sys.exit(1)

    print(f"Successfully loaded {len(images)} images.")
    return np.array(images), np.array(labels)


def build_model(input_shape, num_classes):
    """Builds a CNN model for binary classification."""
    print("Building CNN model...")
    model = keras.Sequential([
        layers.Input(shape=input_shape),
        
        # Block 1
        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        # Block 2
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        # Block 3
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        # Classifier
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
    ])
    
    if num_classes == 2:
        model.add(layers.Dense(1, activation='sigmoid'))
    else:
        model.add(layers.Dense(num_classes, activation='softmax'))

    return model


def plot_history(history, save_path="training_history.png"):
    """Saves training history plot."""
    print("Plotting training history...")
    
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    
    epochs_range = range(len(acc))
    
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')
    
    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    
    plt.savefig(save_path)
    print(f"Saved training history plot to '{save_path}'")
    plt.close()
    
    return save_path


if __name__ == "__main__":
    # Configuration
    IMAGE_DIR = "../data/images"
    IMAGE_SIZE = (256, 256)
    TEST_SPLIT_SIZE = 0.2
    RANDOM_SEED = 42
    BATCH_SIZE = 32
    EPOCHS = 15
    
    # MLflow setup
    mlflow.set_experiment("dandelion_grass_classification")
    
    with mlflow.start_run(run_name=f"cnn_training_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
        
        # Log parameters
        mlflow.log_param("image_size", IMAGE_SIZE)
        mlflow.log_param("test_split", TEST_SPLIT_SIZE)
        mlflow.log_param("batch_size", BATCH_SIZE)
        mlflow.log_param("epochs", EPOCHS)
        mlflow.log_param("random_seed", RANDOM_SEED)
        
        # 1. Load Data
        X, y = load_data(IMAGE_DIR, IMAGE_SIZE)
        mlflow.log_param("total_samples", len(X))
        
        # 2. Encode Labels
        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(y)
        num_classes = len(label_encoder.classes_)
        
        print(f"Found {num_classes} classes: {label_encoder.classes_}")
        mlflow.log_param("num_classes", num_classes)
        mlflow.log_param("classes", str(label_encoder.classes_))
        
        # 3. Split Data
        print(f"Splitting data: {1-TEST_SPLIT_SIZE:.0%} train, {TEST_SPLIT_SIZE:.0%} validation...")
        X_train, X_val, y_train, y_val = train_test_split(
            X, y_encoded, 
            test_size=TEST_SPLIT_SIZE, 
            random_state=RANDOM_SEED,
            stratify=y_encoded
        )
        
        print(f"Training samples: {len(X_train)}")
        print(f"Validation samples: {len(X_val)}")
        mlflow.log_param("train_samples", len(X_train))
        mlflow.log_param("val_samples", len(X_val))
        
        # 4. Build Model
        input_shape = (IMAGE_SIZE[0], IMAGE_SIZE[1], 3)
        model = build_model(input_shape, num_classes)
        
        # 5. Compile Model
        if num_classes == 2:
            model.compile(
                optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy']
            )
            mlflow.log_param("loss", "binary_crossentropy")
        else:
            model.compile(
                optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy']
            )
            mlflow.log_param("loss", "sparse_categorical_crossentropy")
            
        model.summary()
        
        # 6. Train Model
        print("\nStarting model training...")
        history = model.fit(
            X_train, y_train,
            epochs=EPOCHS,
            batch_size=BATCH_SIZE,
            validation_data=(X_val, y_val),
            verbose=1
        )
        print("Training complete.")
        
        # 7. Evaluate
        val_loss, val_acc = model.evaluate(X_val, y_val)
        print(f"\nFinal Validation Accuracy: {val_acc*100:.2f}%")
        print(f"Final Validation Loss: {val_loss:.4f}")
        
        # Log final metrics
        mlflow.log_metric("final_val_accuracy", val_acc)
        mlflow.log_metric("final_val_loss", val_loss)
        mlflow.log_metric("final_train_accuracy", history.history['accuracy'][-1])
        mlflow.log_metric("final_train_loss", history.history['loss'][-1])
        
        # 8. Save Plot
        plot_path = plot_history(history)
        mlflow.log_artifact(plot_path)
        
        # 9. Save Model
        model_filename = "models/dandelion_grass_cnn.keras"
        model.save(model_filename)
        print(f"Model saved to '{model_filename}'")
        
        # Log model with MLflow
        mlflow.keras.log_model(model, "model")
        
        # Log model file as artifact
        mlflow.log_artifact(model_filename)
        
        # Register model in MLflow Model Registry
        model_name = "dandelion-grass-classifier"
        run_id = mlflow.active_run().info.run_id
        model_uri = f"runs:/{run_id}/model"
        
        try:
            # Register the model
            model_version = mlflow.register_model(model_uri, model_name)
            print(f"\n✅ Model registered in MLflow Model Registry!")
            print(f"   Model name: {model_name}")
            print(f"   Version: {model_version.version}")
        except Exception as e:
            print(f"\n⚠️  Could not register model: {e}")
            print(f"   You can register it manually via MLflow UI")
        
        print(f"\n✅ MLflow run completed. Check MLflow UI for details.")
        print(f"Run ID: {run_id}")

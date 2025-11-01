#!/usr/bin/env python3
"""
Script to download and clean images from GitHub repository.
Combines the functionality from MLops_import_clean_images.ipynb
"""

import requests
import pandas as pd
import io
import time
import os
from pathlib import Path
from PIL import Image, UnidentifiedImageError
import sys


def get_image_urls_from_github_folder(repo_api_url):
    """
    Uses the GitHub API to get a list of all file download URLs in a folder.
    """
    print(f"Contacting GitHub API at: {repo_api_url}")
    try:
        response = requests.get(repo_api_url)
        response.raise_for_status()  # Check for errors
        
        file_list = response.json()
        
        if not isinstance(file_list, list):
            print("Error: Failed to get a valid file list from GitHub.")
            print("Response:", file_list.get("message", "Unknown error"))
            return []

        image_urls = []
        for file_info in file_list:
            if file_info.get('type') == 'file' and file_info.get('download_url'):
                # Check for image extensions
                if file_info['name'].lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_urls.append((file_info['name'], file_info['download_url']))
                    
        print(f"Found {len(image_urls)} image files in the repository folder.")
        return image_urls
        
    except requests.exceptions.RequestException as e:
        print(f"Error contacting GitHub API: {e}")
        return []


def download_images(image_list, save_dir):
    """
    Downloads images from a list of (filename, url) tuples.
    """
    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)
    
    print(f"Saving images to '{save_dir}'...")
    
    success_count = 0
    fail_count = 0
    total = len(image_list)
    
    for i, (filename, url) in enumerate(image_list):
        print(f"Downloading {i+1}/{total}: {filename}", end='\r')
        file_save_path = save_path / filename
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            with open(file_save_path, 'wb') as f:
                f.write(response.content)
            
            success_count += 1
            
        except requests.exceptions.RequestException as e:
            print(f"\nFailed to download {filename} from {url}: {e}")
            fail_count += 1
        
        # Be polite to the server
        time.sleep(0.01)

    # Clear the progress line
    print(" " * 80, end='\r')
    print("\n" + "="*30)
    print("Download complete.")
    print(f"Successfully downloaded: {success_count}")
    print(f"Failed to download:    {fail_count}")
    print("="*30)


def clean_and_process_images():
    """
    Scans subdirectories, cleans images, and saves them to a single
    combined output folder, ready for machine learning.
    """
    print("\nStarting image cleaning and processing...")
    
    # Configuration
    SOURCE_BASE_DIR = "image_data_from_repo"
    CATEGORIES = ["dandelion", "grass"]
    OUTPUT_DIR = "cleaned_images_for_model"
    IMAGE_SIZE = (256, 256)
    
    source_base_path = Path(SOURCE_BASE_DIR)
    output_path = Path(OUTPUT_DIR)
    
    # Create the single output directory
    output_path.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    fail_count = 0
    total_processed = 0

    if not source_base_path.exists():
        print(f"Error: Source directory not found: '{SOURCE_BASE_DIR}'")
        print("Please run the download step first.")
        sys.exit(1)

    # Loop through each category (e.g., "dandelion", "grass")
    for category in CATEGORIES:
        category_path = source_base_path / category
        print(f"\nProcessing folder: {category_path}")
        
        if not category_path.exists():
            print(f"Warning: Category folder not found: '{category_path}'. Skipping.")
            continue
            
        image_files = os.listdir(category_path)
        print(f"Found {len(image_files)} files.")
        
        # Loop through each image file in the category folder
        for i, filename in enumerate(image_files):
            total_processed += 1
            print(f"  Processing {i+1}/{len(image_files)}: {filename}", end='\r')
            
            source_file_path = category_path / filename
            
            # Create a new, unique filename that includes the category
            new_filename = f"{category}_{filename}"
            output_file_path = output_path / new_filename
            
            try:
                # Open the image
                with Image.open(source_file_path) as img:
                    # 1. Convert to RGB (removes transparency/alpha)
                    cleaned_img = img.convert("RGB")
                    
                    # 2. Resize to the standard size
                    antialiasing_method = Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.Resampling.LANCZOS
                    resized_img = cleaned_img.resize(IMAGE_SIZE, antialiasing_method)
                    
                    # 3. Save the cleaned image to the output folder
                    resized_img.save(output_file_path, "JPEG", quality=90)
                    
                    success_count += 1
                    
            except (IOError, UnidentifiedImageError, OSError) as e:
                print(f"\nFailed to process {source_file_path}: {e}")
                fail_count += 1
            except Exception as e:
                print(f"\nAn unexpected error occurred with {source_file_path}: {e}")
                fail_count += 1
        
        # Clear the line
        print(" " * 80, end='\r')
        print(f"  Finished processing folder: {category}")

    # --- Final Summary ---
    print("\n\n" + "=" * 30)
    print("Image Processing Complete")
    print("=" * 30)
    print(f"Total images found:     {total_processed}")
    print(f"Successfully cleaned:   {success_count}")
    print(f"Failed to process:      {fail_count}")
    print(f"\nAll cleaned images are saved in: '{OUTPUT_DIR}'")


if __name__ == "__main__":
    # Base URL for the GitHub API
    BASE_API_URL = "https://api.github.com/repos/btphan95/greenr-airflow/contents/data/"
    
    # List of folders to download
    FOLDERS_TO_DOWNLOAD = ["dandelion", "grass"]
    
    # Base directory to save all images
    BASE_SAVE_DIR = "image_data_from_repo"
    
    print(f"Starting download for {len(FOLDERS_TO_DOWNLOAD)} folders...")
    print("=" * 40)
    
    for folder_name in FOLDERS_TO_DOWNLOAD:
        print(f"\nProcessing folder: {folder_name}")
        
        # 1. Construct the specific API URL and save directory for this folder
        api_url = BASE_API_URL + folder_name
        download_dir = os.path.join(BASE_SAVE_DIR, folder_name)
        
        # 2. Get the list of image URLs
        image_list = get_image_urls_from_github_folder(api_url)
        
        # 3. If list is not empty, download the images
        if image_list:
            download_images(image_list, download_dir)
        else:
            print(f"No images found in {folder_name} or failed to retrieve list.")
        
        print("-" * 40)
        
    print("\nAll downloads complete.")
    
    # Now clean the images
    clean_and_process_images()

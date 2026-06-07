import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import subprocess
import json
from pathlib import Path

DATA_DIR = "data"
KAGGLE_USERNAME = "your_kaggle_username"
KAGGLE_KEY = "your_kaggle_api_key"

def setup_kaggle_config():
    kaggle_dir = Path.home() / ".kaggle"
    kaggle_dir.mkdir(exist_ok=True)
    
    kaggle_json = {
        "username": KAGGLE_USERNAME,
        "key": KAGGLE_KEY
    }
    
    with open(kaggle_dir / "kaggle.json", "w") as f:
        json.dump(kaggle_json, f)

def download_datasets():
    os.makedirs(DATA_DIR, exist_ok=True)
    
    datasets = [
        "saketk511/world-important-events-ancient-to-modern",
        "nextmillionaire/car-accident-dataset"
    ]
    
    for dataset in datasets:
        subprocess.run([
            "kaggle", "datasets", "download", dataset, 
            "-p", DATA_DIR, "--unzip"
        ], check=False)

def normalize_and_save(csv_file, output_name):
    df = pd.read_csv(csv_file)
    
    numeric_cols = df.select_dtypes(include=['number']).columns
    
    if len(numeric_cols) > 0:
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        scaler = MinMaxScaler()
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    
    output_path = os.path.join(DATA_DIR, output_name)
    df.to_parquet(output_path, engine='pyarrow', compression='snappy')
    
    return output_path

def main():
    setup_kaggle_config()
    download_datasets()
    
    csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    
    for csv_file in csv_files:
        csv_path = os.path.join(DATA_DIR, csv_file)
        
        if 'events' in csv_file.lower() or 'world' in csv_file.lower():
            normalize_and_save(csv_path, "events_normalized.parquet")
        elif 'accident' in csv_file.lower() or 'car' in csv_file.lower():
            normalize_and_save(csv_path, "accidents_normalized.parquet")

if __name__ == "__main__":
    main()
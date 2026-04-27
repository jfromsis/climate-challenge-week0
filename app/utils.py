import pandas as pd
import os

def load_data():
    data_path = "data"
    dfs = []

    # Check if folder exists
    if not os.path.exists(data_path):
        raise FileNotFoundError("❌ 'data/' folder not found")

    for file in os.listdir(data_path):
        if file.endswith("_clean.csv"):  # ✅ correct method
            file_path = os.path.join(data_path, file)

            df = pd.read_csv(file_path)

            # Extract country name
            country = file.split("_")[0]
            df["Country"] = country.capitalize()

            dfs.append(df)

    if not dfs:
        raise ValueError("❌ No *_clean.csv files found in data/")

    return pd.concat(dfs, ignore_index=True)


def preprocess(df):
    # ✅ FIXED HERE
    df["DATE"] = pd.to_datetime(df["DATE"])

    df["Year"] = df["DATE"].dt.year
    df["Month"] = df["DATE"].dt.month

    return df
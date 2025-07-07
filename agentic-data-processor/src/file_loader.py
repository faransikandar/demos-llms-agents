import pandas as pd

def load_file(filepath: str) -> pd.DataFrame:
    if filepath.endswith('.csv'):
        return pd.read_csv(filepath)
    elif filepath.endswith('.parquet'):
        return pd.read_parquet(filepath)
    elif filepath.endswith('.json'):
        return pd.read_json(filepath)
    else:
        raise ValueError(f"Unsupported file type: {filepath}")

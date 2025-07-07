import pandas as pd
from src.file_loader import load_file

def test_load_csv():
    df = load_file("data/input/sample.csv")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

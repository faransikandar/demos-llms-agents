import pandas as pd
from src.transformations import drop_nulls, convert_to_datetime, filter_by_value, redact_column

def test_drop_nulls():
    df = pd.DataFrame({'a': [1, None, 3]})
    df_clean = drop_nulls(df, 'a')
    assert df_clean['a'].isnull().sum() == 0

def test_convert_to_datetime():
    df = pd.DataFrame({'date': ['2020-01-01', '2020-02-01']})
    df = convert_to_datetime(df, 'date')
    assert pd.api.types.is_datetime64_any_dtype(df['date'])

def test_filter_by_value():
    df = pd.DataFrame({'x': [1, 5, 10]})
    df = filter_by_value(df, 'x', min_value=3)
    assert df['x'].min() >= 3

def test_redact_column():
    df = pd.DataFrame({'email': ['a@example.com', 'b@example.com']})
    df = redact_column(df, 'email')
    assert all(df['email'] == '[REDACTED]')

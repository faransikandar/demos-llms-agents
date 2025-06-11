def drop_nulls(df, column):
    return df[df[column].notnull()]

def convert_to_datetime(df, column, format=None):
    df[column] = pd.to_datetime(df[column], format=format)
    return df

def filter_by_value(df, column, min_value=None, max_value=None):
    if min_value is not None:
        df = df[df[column] >= min_value]
    if max_value is not None:
        df = df[df[column] <= max_value]
    return df

def redact_column(df, column):
    df[column] = '[REDACTED]'
    return df

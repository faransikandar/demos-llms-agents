import boto3
from google.cloud import bigquery
from snowflake.connector import connect

def load_to_s3(df, bucket_name, s3_key):
    import io
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)

    s3 = boto3.client('s3')
    s3.upload_fileobj(buffer, bucket_name, s3_key)
    print(f"Uploaded to s3://{bucket_name}/{s3_key}")

def load_to_bigquery(df, table_id):
    client = bigquery.Client()
    job = client.load_table_from_dataframe(df, table_id)
    job.result()
    print(f"Loaded to {table_id}")

def load_to_snowflake(df, table_name, conn_params):
    conn = connect(**conn_params)
    cursor = conn.cursor()

    # Save to temp CSV
    df.to_csv('temp.csv', index=False)
    # Assume stage is prepared
    cursor.execute(f"PUT file://temp.csv @my_stage")
    cursor.execute(f"COPY INTO {table_name} FROM @my_stage FILE_FORMAT = (type = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '\"')")

    conn.close()

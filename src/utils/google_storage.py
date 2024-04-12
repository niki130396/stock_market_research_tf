from io import StringIO

import pandas as pd
from google.cloud.storage import Client


def read_file_from_storage_bucket(bucket_name: str, file_name: str) -> pd.DataFrame:
    """
    Use it if you are reading a csv stored in a cloud storage bucket
    """
    client = Client()

    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    with blob.open("r") as file:
        data = file.read()
        df = pd.read_csv(StringIO(data))
        return df


def write_dataframe_as_csv_to_storage_bucket(bucket_name: str, file_name: str, data: pd.DataFrame):
    csv_buffer = StringIO()
    data.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()

    client = Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    with blob.open("w") as file:
        file.write(csv_data)

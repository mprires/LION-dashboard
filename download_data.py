from io import BytesIO
import boto3
import pandas as pd


def read_excel_from_s3(bucket_name, file_key, aws_access_key_id, aws_secret_access_key):
    s3 = boto3.client('s3',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)

    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    file_content = response['Body'].read()

    with BytesIO(file_content) as file:
        df = pd.read_csv(file)

    return df

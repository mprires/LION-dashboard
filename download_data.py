from io import BytesIO
import boto3
import pandas as pd
import base64


def read_excel_from_s3(bucket_name, file_key, aws_access_key_id, aws_secret_access_key):
    s3 = boto3.client('s3',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)

    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    file_content = response['Body'].read()

    with BytesIO(file_content) as file:
        df = pd.read_csv(file)

    return df


def fetch_image_from_s3(bucket_name, file_key, aws_access_key_id, aws_secret_access_key):
    """
    Fetches an image file from AWS S3.

    Parameters:
    - bucket_name (str): The name of the S3 bucket.
    - file_key (str): The key (path) to the image file in the bucket.
    - aws_access_key_id (str): AWS Access Key ID with permission to access the bucket.
    - aws_secret_access_key (str): AWS Secret Access Key corresponding to the Access Key ID.

    Returns:
    - Image object (BytesIO): BytesIO object containing the image data.
    """
    s3 = boto3.client('s3',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)

    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    image_data = response['Body'].read()
    base64_image = base64.b64encode(image_data).decode('utf-8')

    return base64_image



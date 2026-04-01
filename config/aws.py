from dotenv import load_dotenv
import os
import boto3

#Recordando un poco para poder subir una imagen a S3 se necesita un client y el nombre del Bucket.
load_dotenv()

#Cliente
s3_client = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    endpoint_url=os.getenv("AWS_SECRET_ACCESS_URL"),
)

#Nombre del bucket
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
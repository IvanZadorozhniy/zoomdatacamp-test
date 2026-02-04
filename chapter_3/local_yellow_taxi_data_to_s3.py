import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = "chapter03"

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-"
MONTHS = [f"{i:02d}" for i in range(1, 7)]
DOWNLOAD_DIR = "downloaded_data"

CHUNK_SIZE = 8 * 1024 * 1024

LOCALSTACK_ENDPOINT = "http://localhost:4566"
REGION = "us-east-1"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

s3 = boto3.client(
    "s3",
    endpoint_url=LOCALSTACK_ENDPOINT,
    region_name=REGION,
    aws_access_key_id="test",
    aws_secret_access_key="test",
)


def create_bucket(bucket_name):
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exists")
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code in ("404", "NoSuchBucket"):
            s3.create_bucket(Bucket=bucket_name)
            print(f"Created bucket '{bucket_name}'")
        else:
            raise


def download_file(month):
    url = f"{BASE_URL}{month}.parquet"
    file_path = os.path.join(DOWNLOAD_DIR, f"yellow_tripdata_2024-{month}.parquet")

    try:
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, file_path)
        print(f"Downloaded: {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None


def verify_s3_upload(bucket, key):
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError:
        return False


def upload_to_s3(file_path, max_retries=3):
    key = os.path.basename(file_path)

    for attempt in range(max_retries):
        try:
            print(
                f"Uploading {file_path} to s3://{BUCKET_NAME}/{key} (Attempt {attempt + 1})"
            )

            s3.upload_file(
                Filename=file_path,
                Bucket=BUCKET_NAME,
                Key=key,
                ExtraArgs={"ACL": "private"},
            )

            if verify_s3_upload(BUCKET_NAME, key):
                print(f"Verification successful for {key}")
                return
            else:
                print(f"Verification failed for {key}, retrying...")

        except Exception as e:
            print(f"Upload failed: {e}")

        time.sleep(3)

    print(f"Giving up on {file_path}")


if __name__ == "__main__":
    create_bucket(BUCKET_NAME)

    with ThreadPoolExecutor(max_workers=4) as executor:
        file_paths = list(executor.map(download_file, MONTHS))

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(upload_to_s3, filter(None, file_paths))

    print("All files processed and verified.")

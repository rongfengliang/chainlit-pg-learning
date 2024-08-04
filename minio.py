from chainlit.data import BaseStorageClient
from chainlit.logger import logger
from typing import Dict, Union, Any
import boto3    # type: ignore

class MinioStorageClient(BaseStorageClient):
    """
    Class to enable MinIO storage provider

    params:
        bucket: Bucket name, should be set with public access
        endpoint_url: MinIO server endpoint, defaults to "http://localhost:9000"
        aws_access_key_id: Default is "minioadmin"
        aws_secret_access_key: Default is "minioadmin"
        verify_ssl: Set to True only if not using HTTP or HTTPS with self-signed SSL certificates
    """
    def __init__(self, bucket: str, endpoint_url: str = 'http://localhost:9000', aws_access_key_id: str = 'minioadmin', aws_secret_access_key: str = 'minioadmin', verify_ssl: bool = False):
        try:
            self.bucket = bucket
            self.endpoint_url = endpoint_url
            self.client = boto3.client("s3", endpoint_url=self.endpoint_url, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, verify=verify_ssl)
            logger.info("MinioStorageClient initialized")
        except Exception as e:
            logger.warn(f"MinioStorageClient initialization error: {e}")

    async def upload_file(self, object_key: str, data: Union[bytes, str], mime: str = 'application/octet-stream', overwrite: bool = True) -> Dict[str, Any]:
        try:
            self.client.put_object(Bucket=self.bucket, Key=object_key, Body=data, ContentType=mime)
            url = f"{self.endpoint_url}/{self.bucket}/{object_key}"
            return {"object_key": object_key, "url": url}
        except Exception as e:
            logger.warn(f"MinioStorageClient, upload_file error: {e}")
            return {}
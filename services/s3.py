import boto3
from decouple import config

from .base_service import BaseService


class S3Service(BaseService):
    def __init__(self):
        super().__init__()
        self.s3 = boto3.client(
            "s3", aws_access_key_id=self.key, aws_secret_access_key=self.secret_key
        )
        self.bucket = config("AWS_BUCKET_NAME")
        self.region = config("AWS_REGION")

    def upload(self, path, key, ext):
        self.s3.upload_file(
            path,
            self.bucket,
            key,
            ExtraArgs={"ACL": "public-read", "ContentType": f"image/{ext}"},
        )

        return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{key}"

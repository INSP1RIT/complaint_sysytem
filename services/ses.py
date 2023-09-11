import boto3

from decouple import config
from .base_service import BaseService


class SESService(BaseService):
    def __init__(self):
        super().__init__()
        self.ses = boto3.client(
            "ses",
            region_name=config("SES_REGION"),
            aws_access_key_id=self.key,
            aws_secret_access_key=self.secret_key,
        )
        self.sender = "abisher72@gmail.com"

    def send_mail(self, subject, to_addresses, text_data):
        body = {"Text": {"Data": text_data, "Charset": "UTF-8"}}
        self.ses.send_email(
            Source=self.sender,
            Destination={
                "ToAddresses": to_addresses,
                "CcAddresses": [],
                "BccAddresses": [],
            },
            Message={"Subject": {"Data": subject, "Charset": "UTF-8"}, "Body": body},
        )

from decouple import config


class BaseService:
    def __init__(self):
        self.key = config("AWS_ACCESS_KEY")
        self.secret_key = config("AWS_SECRET_KEY")

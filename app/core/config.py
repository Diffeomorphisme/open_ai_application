from pydantic import BaseSettings

import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    PAYLOAD_CMS_TOKEN: str = os.getenv("PAYLOAD_CMS_TOKEN")
    URL_CMS: str = os.getenv("URL_CMS")
    OPENAI_APIKEY: str = os.getenv("OPENAI_APIKEY")


settings = Settings()
import os
from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass

load_dotenv(find_dotenv())
@dataclass(frozen=True)
class APIkeys:
    weatherAPI: str = os.getenv('weatherAPI')
    cryptoAPI: str = os.getenv('cryptoAPI')
    stockAPI: str = os.getenv('stockAPI')
    APIKey: str = os.getenv('APIKey')
    APIKeySecret: str = os.getenv('APIKeySecret')
    BearerToken: str = os.getenv('BearerToken')
    AccessToken: str = os.getenv('AccessToken')
    AccessTokenSecret: str = os.getenv('AccessTokenSecret')
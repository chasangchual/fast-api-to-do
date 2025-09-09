from typing import Any

from pydantic import BaseModel, Field
from datetime import datetime, timedelta, timezone

DEFAULT_ACCESS_TOKEN_EXPIRES_IN_SECONDS = 3600
DEFAULT_REFRESH_TOKEN_EXPIRES_IN_DAYS = 7

DEFAULT_ACCESS_TOKEN_EXPIRES_IN = timedelta(minutes=DEFAULT_ACCESS_TOKEN_EXPIRES_IN_SECONDS)
DEFAULT_REFRESH_TOKEN_EXPIRES_IN = timedelta(days=DEFAULT_REFRESH_TOKEN_EXPIRES_IN_DAYS)

BEARER_TOKEN_PREFIX = "Bearer"

class JwtTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "e77b0399-5306-4b7b-9cc2-9ca89211585b",
                "refresh_token": "e77b0399-5306-4b7b-9cc2-9ca89211585b",
                "token_type": "bearer"
            }
        }
    }

    def __init__(self, access_token: str, refresh_token: str, expires_in: int, token_type: str):
        token_data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": expires_in,
            "token_type": token_type
        }
        super().__init__(**token_data)


class JwtBearerTokenResponse(JwtTokenResponse):
    refresh_token: str

    def __init__(self, access_token: str, refresh_token: str, expires_in: int):
        super().__init__(access_token, refresh_token, expires_in, BEARER_TOKEN_PREFIX)

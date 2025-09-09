from typing import Any

from pydantic import BaseModel, Field

class JwtTokenResponse(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "e77b0399-5306-4b7b-9cc2-9ca89211585b",
                "refresh_token": "e77b0399-5306-4b7b-9cc2-9ca89211585b",
                "token_type": "bearer"
            }
        }
    }

    def __init__(self, access_token: str, refresh_token: str, token_type: str):
        token_data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": token_type
        }

        super().__init__(**token_data)

class JwtBearerTokenResponse(JwtTokenResponse):
    refresh_token: str

    def __init__(self, access_token: str, refresh_token: str):
        super().__init__(access_token, refresh_token, "bearer")

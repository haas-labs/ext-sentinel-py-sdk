from pydantic import BaseModel


class Token(BaseModel):
    """
    Token
    """

    access_token: str
    expires_in: int
    refresh_expires_in: int
    token_type: str
    not_before_policy: int
    scope: str

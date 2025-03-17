from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.auth_handler import decode_token

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials or not self.verify_jwt(credentials.credentials):
            raise HTTPException(status_code=403, detail="Invalid token")
        return credentials.credentials

    def verify_jwt(self, token: str) -> bool:
        return decode_token(token) is not None

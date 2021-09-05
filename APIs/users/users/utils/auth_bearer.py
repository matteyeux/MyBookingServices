from fastapi import HTTPException
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from .auth_handler import decodeJWT


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(
            request,
        )
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403,
                    detail="Invalid authentication scheme.",
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403,
                    detail="Invalid token or expired token.",
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403,
                detail="Invalid authorization code.",
            )

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except Exception as e:
            print(e)
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid

    def is_user_admin(self, jwtoken: str) -> str:
        if not self.verify_jwt(jwtoken):
            return ""

        payload = decodeJWT(jwtoken)
        print(payload)
        return ""

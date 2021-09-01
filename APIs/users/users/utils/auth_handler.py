import time
from typing import Dict

import jwt


JWT_SECRET = "please_please_update_me_please"  # config("secret")
JWT_ALGORITHM = "HS256"  # config("algorithm")


def token_response(token: str):
    return {
        "access_token": token,
    }


def signJWT(user_email: str, user_role: str) -> Dict[str, str]:
    payload = {
        "email": user_email,
        "expires": time.time() + 600,
        "role": user_role,
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
        )
        return (
            decoded_token if decoded_token["expires"] >= time.time() else None
        )
    except Exception as e:
        print(e)
        return {}

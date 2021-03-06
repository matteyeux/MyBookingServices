import time
from typing import Dict

import jwt


JWT_SECRET = "please_please_update_me_please"  # config("secret")
JWT_ALGORITHM = "HS256"  # config("algorithm")


def token_response(token: str):
    return {
        "access_token": token,
    }


def signJWT(user_role: str, user_email: str) -> Dict[str, str]:
    payload = {
        "role": user_role,
        "email": user_email,
        "expires": time.time() + 6000,
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

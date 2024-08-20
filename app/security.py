import os

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError

GH_APPLICATION_ID = os.environ.get("GH_APPLICATION_ID", "NONE")
GH_CLIENT_ID = os.environ.get("GH_CLIENT_ID", "NONE")
GH_SECRET = os.environ.get("GH_SECRET", "NONE")
GOOGLE_SECRET = os.environ.get("GOOGLE_SECRET", "NONE")

security = HTTPBearer()
ALGORITHM = "HS256"


def http_validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload  = None
    for secret in [GH_SECRET, GOOGLE_SECRET]:
        try:
            payload = jwt.decode(credentials.credentials, secret, algorithms=[ALGORITHM])
            break
        except InvalidTokenError:
            pass
    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub", None)
    if username is None:
        raise credentials_exception
    return payload

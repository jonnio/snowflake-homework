import json
import os

import requests
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

GH_APPLICATION_ID = os.environ.get("GH_APPLICATION_ID", "NONE")
GH_CLIENT_ID = os.environ.get("GH_CLIENT_ID", "NONE")
GH_SECRET = os.environ.get("GH_SECRET", "NONE")

security = HTTPBearer()


def http_validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    response = requests.post(f'https://api.github.com/applications/{GH_APPLICATION_ID}/token'
                             , headers={"Accept": "application/vnd.github+json",
                                        "X-GitHub-Api-Version": "2022-11-28", }
                             , auth=(GH_CLIENT_ID, GH_SECRET)
                             , json={"access_token": credentials.credentials}
                             )
    return json.loads(response.text) if 200 == response.status_code else ''

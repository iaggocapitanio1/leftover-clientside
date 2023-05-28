import logging.config
from pathlib import Path
from typing import Literal, Union, Optional
import requests
from requests_auth import OAuth2ClientCredentials, OAuth2, JsonTokenFileCache

import settings

OAuth2.token_cache = JsonTokenFileCache('./cache.json')
logging.config.dictConfig(settings.LOGGER)
logger = logging.getLogger(__name__)

oauth = OAuth2ClientCredentials(
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_SECRET,
    token_url=settings.TOKEN_URL,
    scope=["read", "write"]
)

"""REST client handling, including ActionKitStream base class."""

from __future__ import annotations

import typing as t
from requests.auth import HTTPBasicAuth
from singer_sdk.streams import RESTStream

class ActionKitStream(RESTStream):
    """ActionKit stream class."""

    records_jsonpath = "$[*]"
    next_page_token_jsonpath = "$.next_page"

    @property
    def url_base(self) -> str:
        hostname = self.config.get("hostname")
        if not hostname:
            raise ValueError("'hostname' must be provided in the config. Please check your configuration.")
        return f"https://{hostname}.actionkit.com/rest/v1/"

    @property
    def authenticator(self) -> HTTPBasicAuth:
        username = self.config.get("username")
        password = self.config.get("password")
        
        if not username or not password:
            raise ValueError("Both username and password must be provided in the config. Please check your configuration.")
            
        return HTTPBasicAuth(username=username, password=password)

    @property
    def http_headers(self) -> dict:
        return {}

    def get_url_params(self, context: t.Optional[dict], next_page_token: t.Optional[str]) -> t.Dict[str, t.Any]:
        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key
        return params

"""REST client handling, including ActionKitStream base class."""

from __future__ import annotations

import typing as t
from requests.auth import _basic_auth_str
from singer_sdk.streams import RESTStream

class ActionKitStream(RESTStream):
    """ActionKit stream class."""

    records_jsonpath = "$.objects[*]"
    next_page_token_jsonpath = "$.meta.next"
    limit = 100

    @property
    def url_base(self) -> str:
        hostname = self.config.get("hostname")
        if not hostname:
            raise ValueError("'hostname' must be provided in the config. Please check your configuration.")
        return f"https://{hostname}.actionkit.com/rest/v1"

    @property
    def authenticator(self) -> None:
        return None

    @property
    def http_headers(self) -> dict:
        username = self.config.get("username")
        password = self.config.get("password")
        
        if not username or not password:
            raise ValueError("Both username and password must be provided in the config. Please check your configuration.")

        return {"Authorization": _basic_auth_str(username, password)}

    def get_url_params(self, context: t.Optional[dict], next_page_token: t.Optional[str]) -> t.Dict[str, t.Any]:
        params: dict = {}
        if next_page_token:
            offset = next_page_token.split("_offset=")[-1].split("&")[0]
            params["_offset"] = offset
        if self.replication_key:
            params["order_by"] = self.replication_key # if you want the reverse order, use -replication_key
        if self.limit:
            params["_limit"] = self.limit
        params["format"] = "json"

        return params

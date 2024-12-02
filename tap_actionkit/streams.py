"""Stream type classes for tap-actionkit."""

from __future__ import annotations

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_actionkit.client import ActionKitStream


class UsersStream(ActionKitStream):
    """Define custom stream for users."""

    name = "users"
    path = "/user"
    primary_keys = ["id"]
    replication_key = None
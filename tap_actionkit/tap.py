"""ActionKit tap class."""

from __future__ import annotations
from typing import List

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_actionkit.client import ActionKitStream
from tap_actionkit.streams import UsersStream

STREAM_TYPES = [
    UsersStream,
]


class TapActionKit(Tap):
    """ActionKit tap class."""

    name = "tap-actionkit"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "hostname",
            th.StringType,
            required=True,
            description="The ActionKit instance hostname",
        ),
        th.Property(
            "username",
            th.StringType,
            required=True,
            description="API username for authentication",
        ),
        th.Property(
            "password",
            th.StringType,
            required=True,
            description="API password for authentication",
        ),
    ).to_dict()

    def discover_streams(self) -> List[ActionKitStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
    
    def sync_all(self) -> None:
        raise NotImplementedError("Sync all is not implemented")


if __name__ == "__main__":
    TapActionKit.cli()

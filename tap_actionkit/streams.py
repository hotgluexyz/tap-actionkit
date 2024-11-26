"""Stream type classes for tap-actionkit."""

from __future__ import annotations

import typing as t

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_actionkit.client import ActionKitStream


class ContactsStream(ActionKitStream):
    """Define custom stream for contacts."""

    name = "contacts"
    path = "/contacts"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("first_name", th.StringType),
        th.Property("last_name", th.StringType),
        th.Property(
            "email",
            th.StringType,
            description="The contact's email address",
        ),
        th.Property(
            "phone_numbers",
            th.ArrayType(
                th.ObjectType(
                    th.Property("type", th.StringType),
                    th.Property("number", th.StringType),
                )
            ),
            description="List of phone numbers associated with the contact",
        ),
        th.Property(
            "addresses",
            th.ArrayType(
                th.ObjectType(
                    th.Property("line1", th.StringType),
                    th.Property("city", th.StringType),
                    th.Property("state", th.StringType),
                    th.Property("postal_code", th.StringType),
                    th.Property("country", th.StringType),
                )
            ),
            description="List of addresses associated with the contact",
        ),
    ).to_dict()


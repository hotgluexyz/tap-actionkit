"""Stream type classes for tap-actionkit."""

from __future__ import annotations

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_actionkit.client import ActionKitStream


class ContactsStream(ActionKitStream):
    """Define custom stream for contacts."""

    name = "contacts"
    path = "/user"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.objects[*]"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("first_name", th.StringType),
        th.Property("middle_name", th.StringType),
        th.Property("last_name", th.StringType),
        th.Property("useroriginal", th.StringType),
        th.Property("suffix", th.StringType),
        th.Property("phones", th.ArrayType(th.StringType)),
        th.Property("updated_at", th.DateTimeType),
        th.Property("actions", th.StringType),
        th.Property("prefix", th.StringType),
        th.Property("orders", th.StringType),
        th.Property("city", th.StringType),
        th.Property("zip", th.StringType),
        th.Property("rand_id", th.IntegerType),
        th.Property("subscriptionhistory", th.StringType),
        th.Property("source", th.StringType),
        th.Property("state", th.StringType),
        th.Property("location", th.StringType),
        th.Property("logintoken", th.StringType),
        th.Property("subscription_status", th.StringType),
        th.Property("email", th.StringType),
        th.Property("subscriptions", th.StringType),
        th.Property("address1", th.StringType),
        th.Property("address2", th.StringType),
        th.Property("orderrecurrings", th.StringType),
        th.Property("eventsignups", th.StringType),
        th.Property("postal", th.StringType),
        th.Property("lang", th.StringType),
        th.Property("plus4", th.StringType),
        th.Property("fields", th.CustomType({"type": ["object", "string"]})),
        th.Property("created_at", th.DateTimeType),
        th.Property("events", th.StringType),
        th.Property("token", th.StringType),
        th.Property("usermailings", th.StringType),
        th.Property("country", th.StringType),
        th.Property("region", th.StringType),
        th.Property("resource_uri", th.StringType),
    ).to_dict()


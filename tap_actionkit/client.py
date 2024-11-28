"""REST client handling, including ActionKitStream base class."""

from datetime import datetime

from functools import cached_property
import typing as t
import requests
from requests.auth import _basic_auth_str
from singer_sdk.streams import RESTStream
from singer_sdk import typing as th
from pendulum import parse

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

    def get_starting_time(self, context):
        start_date = self.config.get("start_date")
        if start_date:
            start_date = parse(self.config.get("start_date"))
        rep_key = self.get_starting_timestamp(context)
        return rep_key or start_date

    def is_unix_timestamp(self, date):
        try:
            datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
            return True
        except:
            return False

    def get_jsonschema_type(self, obj):
        dtype = type(obj)

        if dtype == int:
            return th.IntegerType()
        if dtype == float:
            return th.NumberType()
        if dtype == str:
            if self.is_unix_timestamp(obj):
                return th.DateTimeType()
            return th.StringType()
        if dtype == bool:
            return th.BooleanType()
        if dtype == list:
            if len(obj) > 0:
                return th.ArrayType(self.get_jsonschema_type(obj[0]))
            else:
                return th.ArrayType(
                    th.CustomType({"type": ["number", "string", "object"]})
                )
        if dtype == dict:
            obj_props = []
            for key in obj.keys():
                obj_props.append(th.Property(key, self.get_jsonschema_type(obj[key])))
            return th.ObjectType(*obj_props)
        else:
            return th.CustomType({"type": ["number", "string", "object"]})

    def get_schema(self) -> dict:
        """Dynamically detect the json schema for the stream.
        This is evaluated prior to any records being retrieved.
        """
        context = {}
        self._requests_session = requests.Session()
        decorated_request = self.request_decorator(self._request)
        prepared_request = self.prepare_request(context=context, next_page_token=None)
        resp = decorated_request(prepared_request, context)
        records_gen = self.parse_response(resp)
        record = next(records_gen, None)
        if record is None or len(record) == 0:
            return th.PropertiesList(
                th.Property("id", th.StringType),
                th.Property(self.replication_key, th.DateTimeType),
            ).to_dict()
        
        properties = []
        property_names = set()
        custom_fields_dict: dict[str, list[th.Property]] = {"fields": {}}
        for record in records_gen:
            for name in record.keys():
                if name in property_names and name not in custom_fields_dict:
                    continue
                # Add the new property to our list
                property_names.add(name)
                if name in custom_fields_dict:
                    for custom_field_name, custom_field_value in record[name].items():
                        custom_fields_dict[name][custom_field_name] = self.get_jsonschema_type(custom_field_value)
                else:
                    properties.append(
                        th.Property(name, self.get_jsonschema_type(record[name]))
                    )
        
        for name, custom_fields in custom_fields_dict.items():
            properties.append(
                th.Property(name, th.ObjectType(*[th.Property(cf_name, cf_type) for cf_name, cf_type in custom_fields.items()]))
            )
        # if the rep_key is not at a header level add updated as default
        if (
            self.replication_key is not None
            and self.replication_key not in record.keys()
        ):
            properties.append(
                th.Property(self.replication_key, th.DateTimeType)
            )
        # Return the list as a JSON Schema dictionary object
        property_list = th.PropertiesList(*properties).to_dict()

        return property_list

    @cached_property
    def schema(self) -> dict:
        return self.get_schema()

from tap_aftership.streams.abstracts import FullTableStream

class Roles(FullTableStream):
    tap_stream_id = "roles"
    key_properties = ["code"]
    replication_method = "FULL_TABLE"
    data_key = "roles"
    path = "admin/{api_version}/roles"


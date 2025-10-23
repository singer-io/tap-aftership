from tap_aftership.streams.abstracts import FullTableStream

class Memberships(FullTableStream):
    tap_stream_id = "memberships"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    data_key = "memberships"
    api_version = "2022-01"
    path = f"admin/{api_version}/memberships"

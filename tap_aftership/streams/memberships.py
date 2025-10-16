from tap_aftership.streams.abstracts import FullTableStream

class Memberships(FullTableStream):
    tap_stream_id = "memberships"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    data_key = "memberships"
    path = "admin/{api_version}/memberships"


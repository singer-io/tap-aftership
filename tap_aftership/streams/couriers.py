from tap_aftership.streams.abstracts import FullTableStream

class Couriers(FullTableStream):
    tap_stream_id = "couriers"
    key_properties = ["slug"]
    replication_method = "FULL_TABLE"
    data_key = "couriers"
    path = "tracking/{api_version}/couriers"


from tap_aftership.streams.abstracts import IncrementalStream

class Pickups(IncrementalStream):
    tap_stream_id = "pickups"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "pickups"
    path = "pickups"


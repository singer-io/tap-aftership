from tap_aftership.streams.abstracts import IncrementalStream

class CancelPickups(IncrementalStream):
    tap_stream_id = "cancel_pickups"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "cancel_pickups"
    path = "cancel-pickups"


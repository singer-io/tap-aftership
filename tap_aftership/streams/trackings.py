from tap_aftership.streams.abstracts import IncrementalStream

class Trackings(IncrementalStream):
    tap_stream_id = "trackings"
    key_properties = "id"
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "trackings"
    path = "tracking/{api_version}/trackings"


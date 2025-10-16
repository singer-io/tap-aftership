from tap_aftership.streams.abstracts import IncrementalStream

class CourierConnections(IncrementalStream):
    tap_stream_id = "courier_connections"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "courier_connections"
    path = "tracking/{api_version}/courier-connections"


from tap_aftership.streams.abstracts import IncrementalStream

class CourierConnections(IncrementalStream):
    tap_stream_id = "courier_connections"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "courier_connections"
    api_version = "2025-07"
    path = f"tracking/{api_version}/courier-connections"
    next_page_param = "cursor"
    next_page_key = "pagination.next_cursor"

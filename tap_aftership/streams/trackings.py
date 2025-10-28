from tap_aftership.streams.abstracts import IncrementalStream

class Trackings(IncrementalStream):
    tap_stream_id = "trackings"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "trackings"
    api_version = "2025-07"
    path = f"tracking/{api_version}/trackings"
    next_page_param = "cursor"
    next_page_key = "pagination.next_cursor"

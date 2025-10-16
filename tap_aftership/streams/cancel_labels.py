from tap_aftership.streams.abstracts import IncrementalStream

class CancelLabels(IncrementalStream):
    tap_stream_id = "cancel_labels"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "cancel_labels"
    path = "/cancel-labels"


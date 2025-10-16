from tap_aftership.streams.abstracts import IncrementalStream

class ShippingLabels(IncrementalStream):
    tap_stream_id = "shipping_labels"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "labels"
    path = "labels"


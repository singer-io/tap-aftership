from tap_aftership.streams.abstracts import IncrementalStream, ShippingMixin

class ShippingLabels(ShippingMixin, IncrementalStream):
    tap_stream_id = "shipping_labels"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "labels"
    path = "labels"
    next_page_param = "next_token"
    next_page_key = "next_token"

from tap_aftership.streams.abstracts import IncrementalStream, ShippingMixin

class Pickups(ShippingMixin, IncrementalStream):
    tap_stream_id = "pickups"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "pickups"
    path = "pickups"
    next_page_param = "next_token"
    next_page_key = "next_token"
    use_created_at_min = True

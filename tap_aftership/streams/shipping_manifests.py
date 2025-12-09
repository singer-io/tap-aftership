from tap_aftership.streams.abstracts import IncrementalStream, ShippingMixin

class ShippingManifests(ShippingMixin, IncrementalStream):
    tap_stream_id = "shipping_manifests"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "manifests"
    path = "manifests"
    next_page_param = "next_token"
    next_page_key = "next_token"

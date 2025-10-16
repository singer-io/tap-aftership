from tap_aftership.streams.abstracts import IncrementalStream

class ShippingManifests(IncrementalStream):
    tap_stream_id = "shipping_manifests"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "manifests"
    path = "manifests"


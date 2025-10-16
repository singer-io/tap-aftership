from tap_aftership.streams.abstracts import IncrementalStream

class ShippingRates(IncrementalStream):
    tap_stream_id = "shipping_rates"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "rates"
    path = "rates"


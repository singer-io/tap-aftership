from tap_aftership.streams.abstracts import IncrementalStream, ShippingMixin

class ShippingRates(ShippingMixin, IncrementalStream):
    tap_stream_id = "shipping_rates"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "rates"
    path = "rates"
    next_page_param = "next_token"
    next_page_key = "next_token"
    use_created_at_min = True

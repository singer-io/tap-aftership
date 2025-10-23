from tap_aftership.streams.abstracts import IncrementalStream, ShippingMixin

class ShipperAccounts(ShippingMixin, IncrementalStream):
    tap_stream_id = "shipper_accounts"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "shipper_accounts"
    path = "shipper-accounts"
    next_page_param = "next_token"
    next_page_key = "next_token"

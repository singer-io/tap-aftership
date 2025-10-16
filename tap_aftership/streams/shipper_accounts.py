from tap_aftership.streams.abstracts import IncrementalStream

class ShipperAccounts(IncrementalStream):
    tap_stream_id = "shipper_accounts"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "shipper_accounts"
    path = "shipper-accounts"


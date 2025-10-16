from tap_aftership.streams.abstracts import ChildBaseStream

class Orders(ChildBaseStream):
    tap_stream_id = "orders"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "orders"
    path = "commerce/{api_version}/orders"
    parent = "stores"
    bookmark_value = None


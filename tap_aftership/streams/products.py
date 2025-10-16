from tap_aftership.streams.abstracts import ChildBaseStream

class Products(ChildBaseStream):
    tap_stream_id = "products"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "products"
    path = "commerce/{api_version}/products"
    parent = "stores"
    bookmark_value = None


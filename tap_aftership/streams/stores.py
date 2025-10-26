from tap_aftership.streams.abstracts import ParentBaseStream

class Stores(ParentBaseStream):
    tap_stream_id = "stores"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "stores"
    api_version = "2025-07"
    path = f"commerce/{api_version}/stores"
    children = ["orders", "products", "fulfillments"]
    next_page_param = "page"
    next_page_key = "page"

from tap_aftership.streams.abstracts import ChildBaseStream

class Fulfillments(ChildBaseStream):
    tap_stream_id = "fulfillments"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    api_version = "2025-07"
    path = f"commerce/{api_version}/fulfillments"
    parent = "stores"
    bookmark_value = None

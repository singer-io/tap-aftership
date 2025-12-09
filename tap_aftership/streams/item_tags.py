from tap_aftership.streams.abstracts import IncrementalStream

class ItemTags(IncrementalStream):
    tap_stream_id = "item_tags"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["created_at"]
    data_key = "item_tags"
    api_version = "2025-07"
    path = f"returns/{api_version}/item-tags"

from typing import Dict
from tap_aftership.streams.abstracts import ChildBaseStream

class Orders(ChildBaseStream):
    tap_stream_id = "orders"
    key_properties = ["id", "store_id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "orders"
    api_version = "2025-07"
    path = f"commerce/{api_version}/orders"
    parent = "stores"
    bookmark_value = None
    next_page_param = "page"
    next_page_key = "page"

    def update_headers(self, **kwargs) -> None:
        """Update headers for the stream."""
        parent = kwargs.get("parent_obj")
        if parent and "id" in parent:
            self.headers["as-store-id"] = parent["id"]

    def modify_object(self, record: Dict, parent_record: Dict = None) -> Dict:
        """
        Modify the record before writing to the stream
        """
        store = record.get("store")
        if store and "id" in store:
            record["store_id"] = store["id"]
        return record
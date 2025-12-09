from typing import Dict
from tap_aftership.streams.abstracts import ChildBaseStream

class Fulfillments(ChildBaseStream):
    tap_stream_id = "fulfillments"
    key_properties = ["id", "store_id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "fulfillments"
    api_version = "2025-07"
    path = f"commerce/{api_version}/fulfillments"
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
        store_id = parent_record.get("id")
        if store_id:
            record["store_id"] = store_id
        return record
from typing import Dict
from tap_aftership.streams.abstracts import ChildBaseStream

class Fulfillments(ChildBaseStream):
    tap_stream_id = "fulfillments"
    key_properties = ["id", "store_id", "order_id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "fulfillments"
    api_version = "2025-07"
    path = f"commerce/{api_version}/fulfillments"
    parent = "orders"
    bookmark_value = None
    next_page_param = "page"
    next_page_key = "page"
    page_size = 50

    def update_headers(self, **kwargs) -> None:
        """Update headers for the stream."""
        parent = kwargs.get("parent_obj")
        if parent and "store_id" in parent:
            self.headers["as-store-id"] = parent["store_id"]

    def update_params(self, state = None, parent_obj = None, **kwargs):
        """Update params for the stream."""
        kwargs.update({"order_id": parent_obj.get("id")})
        return super().update_params(state, parent_obj, **kwargs)

    def modify_object(self, record: Dict, parent_record: Dict = None) -> Dict:
        """
        Modify the record before writing to the stream
        """
        store_id = parent_record.get("store_id")
        if store_id:
            record["store_id"] = store_id
        return record
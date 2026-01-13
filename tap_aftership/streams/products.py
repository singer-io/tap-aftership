from typing import Dict
from tap_aftership.streams.abstracts import FullTableStream

class Products(FullTableStream):
    tap_stream_id = "products"
    key_properties = ["id", "store_id"]
    replication_method = "FULL_TABLE"
    data_key = "products"
    api_version = "2025-07"
    path = f"commerce/{api_version}/products"
    parent = "stores"
    bookmark_value = None
    next_page_param = "page"
    next_page_key = "page"
    page_size = 50

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

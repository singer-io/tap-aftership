from tap_aftership.streams.abstracts import FullTableStream

class ItemReturns(FullTableStream):
    tap_stream_id = "item_returns"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    data_key = "returns"
    api_version = "2025-07"
    path = f"returns/{api_version}/returns"
    next_page_param = "page"
    next_page_key = "page"

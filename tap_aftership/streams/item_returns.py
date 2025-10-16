from tap_aftership.streams.abstracts import FullTableStream

class ItemReturns(FullTableStream):
    tap_stream_id = "item_returns"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    data_key = "returns"
    path = "returns/{api_version}/returns"


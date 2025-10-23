from tap_aftership.streams.abstracts import IncrementalStream

class QueryCoverages(IncrementalStream):
    tap_stream_id = "query_coverages"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "coverages"
    api_version = "2022-01"
    path = f"admin/{api_version}/coverages"

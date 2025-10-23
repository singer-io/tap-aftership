from tap_aftership.streams.abstracts import IncrementalStream

class QueryClaims(IncrementalStream):
    tap_stream_id = "query_claims"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "claims"
    api_version = "2022-01"
    path = f"admin/{api_version}/claims"

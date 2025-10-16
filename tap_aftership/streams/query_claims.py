from tap_aftership.streams.abstracts import IncrementalStream

class QueryClaims(IncrementalStream):
    tap_stream_id = "query_claims"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "claims"
    path = "admin/{api_version}/claims"


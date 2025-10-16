from tap_aftership.streams.abstracts import FullTableStream

class Locations(FullTableStream):
    tap_stream_id = "locations"
    key_properties = ["location_id"]
    replication_method = "FULL_TABLE"
    data_key = "locations"
    path = "locations"


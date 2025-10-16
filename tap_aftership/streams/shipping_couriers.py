from tap_aftership.streams.abstracts import FullTableStream

class ShippingCouriers(FullTableStream):
    tap_stream_id = "shipping_couriers"
    key_properties = ["slug"]
    replication_method = "FULL_TABLE"
    data_key = "couriers"
    path = "couriers"


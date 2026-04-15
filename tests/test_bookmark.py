from base import AftershipBaseTest, NO_READ_PERMISSION_STREAMS
from tap_tester.base_suite_tests.bookmark_test import BookmarkTest


class AftershipBookmarkTest(BookmarkTest, AftershipBaseTest):
    """Test tap sets a bookmark and respects it for the next sync of a
    stream."""
    bookmark_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    initial_bookmarks = {
        "bookmarks": {
            "trackings": { "updated_at" : "2020-01-01T00:00:00Z"},
            "stores": { "updated_at" : "2020-01-01T00:00:00Z"},
            "shipper_accounts": { "updated_at" : "2020-01-01T00:00:00Z"},
        }
    }
    @staticmethod
    def name():
        return "tap_tester_aftership_bookmark_test"

    def expected_stream_names(self):
        return super().expected_stream_names().difference(NO_READ_PERMISSION_STREAMS)

    def streams_to_test(self):
        # streams to exclude due to access or insufficient data for bookmark test
        no_data_or_full_table_streams = {
            "couriers",          # Full table stream, not incremental
            "courier_connections",
            "orders",
            "fulfillments",
            "products",          # Full table child stream, not incremental
            "shipping_rates",
            "shipping_labels",   # Only 1 unique replication value - not enough for bookmark test
            "shipping_manifests",
            "shipping_couriers",
            "cancel_labels",
            "pickups",
            "cancel_pickups",
        }
        return self.expected_stream_names().difference(no_data_or_full_table_streams)

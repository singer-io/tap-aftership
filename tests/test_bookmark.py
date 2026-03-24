from base import aftershipBaseTest
from tap_tester.base_suite_tests.bookmark_test import BookmarkTest


class aftershipBookMarkTest(BookmarkTest, aftershipBaseTest):
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

    def streams_to_test(self):
        # streams to exclude from the start date test due to access or insufficient data
        streams_to_exclude = set({
            "couriers",  # Full table stream, not incremental
            "courier_connections",
            "item_returns",
            "item_tags",
            "query_claims",
            "query_coverages",
            "orders",
            "fulfillments",
            "products",  # Full table child stream, not incremental
            "memberships",
            "roles",
            "shipping_rates",
            "shipping_labels",  # Only 1 unique replication value - not enough for bookmark test
            "shipping_manifests",
            "shipping_couriers",
            "cancel_labels",
            "pickups",
            "cancel_pickups",
            "locations"
        })
        return self.expected_stream_names().difference(streams_to_exclude)


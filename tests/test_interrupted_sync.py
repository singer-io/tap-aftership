
from base import AftershipBaseTest
from tap_tester.base_suite_tests.interrupted_sync_test import InterruptedSyncTest

NO_READ_PERMISSION_STREAMS = {
    "item_returns",
    "item_tags",
    "query_claims",
    "query_coverages",
    "memberships",
    "roles",
    "locations",
}


class AftershipInterruptedSyncTest(InterruptedSyncTest, AftershipBaseTest):
    """Test tap sets a bookmark and respects it for the next sync of a
    stream."""

    @staticmethod
    def name():
        return "tap_tester_aftership_interrupted_sync_test"

    def expected_stream_names(self):
        return super().expected_stream_names().difference(NO_READ_PERMISSION_STREAMS)

    def streams_to_test(self):
        # streams to exclude due to access or insufficient/non-deterministic data
        streams_to_exclude = {
            "courier_connections",
            "orders",          # Data changes between syncs causing test failures
            "products",
            "fulfillments",    # Data changes between syncs causing test failures
            "shipping_rates",
            "shipping_manifests",
            "shipping_couriers",
            "cancel_labels",
            "pickups",
            "cancel_pickups",
            "couriers",
            "trackings",       # API returns records in non-deterministic order
        }
        return self.expected_stream_names().difference(streams_to_exclude)


    def manipulate_state(self):
        return {
            "currently_syncing": "stores",
            "bookmarks": {
                "stores": { "updated_at" : "2020-01-01T00:00:00Z"},
                "shipping_labels": { "updated_at" : "2020-01-01T00:00:00Z"},
                "shipper_accounts": { "updated_at" : "2020-01-01T00:00:00Z"},
        }
    }

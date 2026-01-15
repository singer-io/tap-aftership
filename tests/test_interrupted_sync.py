
from base import aftershipBaseTest
from tap_tester.base_suite_tests.interrupted_sync_test import InterruptedSyncTest


class aftershipInterruptedSyncTest(InterruptedSyncTest, aftershipBaseTest):
    """Test tap sets a bookmark and respects it for the next sync of a
    stream."""

    @staticmethod
    def name():
        return "tap_tester_aftership_interrupted_sync_test"

    def streams_to_test(self):
        # streams to exclude from the start date test due to access or insufficient data
        streams_to_exclude = set({
            "courier_connections",
            "item_returns",
            "item_tags",
            "query_claims",
            "query_coverages",
            "orders",  # Data changes between syncs causing test failures
            "products",
            "fulfillments",  # Data changes between syncs causing test failures
            "memberships",
            "roles",
            "shipping_rates",
            "shipping_manifests",
            "shipping_couriers",
            "cancel_labels",
            "pickups",
            "cancel_pickups",
            "locations",
            "couriers",
            "trackings",  # API returns records in non-deterministic order, causing interrupted sync test to fail
        })
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

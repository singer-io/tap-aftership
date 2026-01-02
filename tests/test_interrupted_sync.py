
from base import aftershipBaseTest
from tap_tester.base_suite_tests.interrupted_sync_test import InterruptedSyncTest


class aftershipInterruptedSyncTest(InterruptedSyncTest, aftershipBaseTest):
    """Test tap sets a bookmark and respects it for the next sync of a
    stream."""

    @staticmethod
    def name():
        return "tap_tester_aftership_interrupted_sync_test"

    def streams_to_test(self):
        streams_to_exclude = {
            "courier_connections",
            "item_returns",
            "item_tags",
            "query_claims",
            "query_coverages",
            "stores",
            "orders",
            "products",
            "fulfillments",
            "memberships",
            "roles",
            "shipping_rates",
            "shipping_labels",
            "shipping_manifests",
            "shipping_couriers",
            "cancel_labels",
            "pickups",
            "cancel_pickups",
            "shipper_accounts",
            "locations"
        }
        return self.expected_stream_names().difference(streams_to_exclude)


    def manipulate_state(self):
        return {
            "currently_syncing": "prospects",
            "bookmarks": {
                "trackings": { "updated_at" : "2020-01-01T00:00:00Z"},
                "courier_connections": { "updated_at" : "2020-01-01T00:00:00Z"},
                "item_tags": { "created_at" : "2020-01-01T00:00:00Z"},
                "query_claims": { "updated_at" : "2020-01-01T00:00:00Z"},
                "query_coverages": { "updated_at" : "2020-01-01T00:00:00Z"},
                "stores": { "updated_at" : "2020-01-01T00:00:00Z"},
                "orders": { "updated_at" : "2020-01-01T00:00:00Z"},
                "products": { "updated_at" : "2020-01-01T00:00:00Z"},
                "fulfillments": { "updated_at" : "2020-01-01T00:00:00Z"},
                "shipping_rates": { "updated_at" : "2020-01-01T00:00:00Z"},
                "shipping_labels": { "updated_at" : "2020-01-01T00:00:00Z"},
                "shipping_manifests": { "updated_at" : "2020-01-01T00:00:00Z"},
                "cancel_labels": { "updated_at" : "2020-01-01T00:00:00Z"},
                "pickups": { "updated_at" : "2020-01-01T00:00:00Z"},
                "cancel_pickups": { "updated_at" : "2020-01-01T00:00:00Z"},
                "shipper_accounts": { "updated_at" : "2020-01-01T00:00:00Z"},
        }
    }


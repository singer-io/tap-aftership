from base import aftershipBaseTest
from tap_tester.base_suite_tests.all_fields_test import AllFieldsTest

KNOWN_MISSING_FIELDS = {

}


class aftershipAllFields(AllFieldsTest, aftershipBaseTest):
    """Ensure running the tap with all streams and fields selected results in
    the replication of all fields."""

    @staticmethod
    def name():
        return "tap_tester_aftership_all_fields_test"

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


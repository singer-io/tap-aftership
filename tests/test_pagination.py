from tap_tester.base_suite_tests.pagination_test import PaginationTest
from base import aftershipBaseTest

class aftershipPaginationTest(PaginationTest, aftershipBaseTest):
    """
    Ensure tap can replicate multiple pages of data for streams that use pagination.
    """

    @staticmethod
    def name():
        return "tap_tester_aftership_pagination_test"

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


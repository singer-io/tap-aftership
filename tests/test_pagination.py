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
        # streams to exclude from the start date test due to access or insufficient data
        streams_to_exclude = set({
            "courier_connections",
            "item_returns",
            "item_tags",
            "query_claims",
            "query_coverages",
            "memberships",
            "roles",
            "shipping_rates",
            "shipping_manifests",
            "shipping_couriers",
            "cancel_labels",
            "pickups",
            "cancel_pickups",
            "locations"
        })
        return self.expected_stream_names().difference(streams_to_exclude)

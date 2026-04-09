from tap_tester.base_suite_tests.pagination_test import PaginationTest
from base import AftershipBaseTest

NO_READ_PERMISSION_STREAMS = {
    "item_returns",
    "item_tags",
    "query_claims",
    "query_coverages",
    "memberships",
    "roles",
    "locations",
}


class AftershipPaginationTest(PaginationTest, AftershipBaseTest):
    """
    Ensure tap can replicate multiple pages of data for streams that use pagination.
    """

    @staticmethod
    def name():
        return "tap_tester_aftership_pagination_test"

    def expected_stream_names(self):
        return super().expected_stream_names().difference(NO_READ_PERMISSION_STREAMS)

    def streams_to_test(self):
        # streams to exclude due to insufficient data in the test environment
        no_data_streams = {
            "courier_connections",
            "shipping_rates",
            "shipping_manifests",
            "shipping_couriers",
            "cancel_labels",
            "pickups",
            "cancel_pickups",
        }
        return self.expected_stream_names().difference(no_data_streams)

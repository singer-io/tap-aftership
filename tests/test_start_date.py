from base import aftershipBaseTest
from tap_tester.base_suite_tests.start_date_test import StartDateTest



class aftershipStartDateTest(StartDateTest, aftershipBaseTest):
    """Instantiate start date according to the desired data set and run the
    test."""

    @staticmethod
    def name():
        return "tap_tester_aftership_start_date_test"

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

    @property
    def start_date_1(self):
        return "2015-03-25T00:00:00Z"
    @property
    def start_date_2(self):
        return "2017-01-25T00:00:00Z"


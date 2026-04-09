from base import AftershipBaseTest
from tap_tester.base_suite_tests.all_fields_test import AllFieldsTest

KNOWN_MISSING_FIELDS = {

}

NO_READ_PERMISSION_STREAMS = {
    "locations",
    "memberships",
    "item_returns",
    "query_claims",
    "query_coverages",
    "item_tags",
    "roles",
}


class AftershipAllFields(AllFieldsTest, AftershipBaseTest):
    """Ensure running the tap with all streams and fields selected results in
    the replication of all fields."""

    @staticmethod
    def name():
        return "tap_tester_aftership_all_fields_test"

    def expected_stream_names(self):
        return super().expected_stream_names().difference(NO_READ_PERMISSION_STREAMS)

    def streams_to_test(self):
        # streams to exclude due to insufficient data in the test environment
        streams_to_exclude = set({
            "courier_connections",
            "shipping_rates",
            "shipping_manifests",
            "cancel_labels",
            "pickups",
            "cancel_pickups",
        })
        return self.expected_stream_names().difference(streams_to_exclude)

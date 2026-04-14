"""Test that with no fields selected for a stream automatic fields are still
replicated."""
from base import AftershipBaseTest, NO_READ_PERMISSION_STREAMS
from tap_tester.base_suite_tests.automatic_fields_test import MinimumSelectionTest


class AftershipAutomaticFields(MinimumSelectionTest, AftershipBaseTest):
    """Test that with no fields selected for a stream automatic fields are
    still replicated."""

    @staticmethod
    def name():
        return "tap_tester_aftership_automatic_fields_test"

    def expected_stream_names(self):
        return super().expected_stream_names().difference(NO_READ_PERMISSION_STREAMS)

    def streams_to_test(self):
        # streams to exclude due to insufficient data in the test environment
        no_data_streams = {
            "courier_connections",
            "shipping_rates",
            "shipping_labels",
            "shipping_manifests",
            "shipping_couriers",
            "cancel_labels",
            "pickups",
            "cancel_pickups",
        }
        return self.expected_stream_names().difference(no_data_streams)

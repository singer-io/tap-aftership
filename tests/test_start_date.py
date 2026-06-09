from base import AftershipBaseTest, NO_READ_PERMISSION_STREAMS
from tap_tester.base_suite_tests.start_date_test import StartDateTest


class AftershipStartDateTest(StartDateTest, AftershipBaseTest):
    """Instantiate start date according to the desired data set and run the
    test."""

    # Per-class sync cache – isolates this class from other StartDateTest
    # subclasses that also store results on the shared StartDateTest attributes.
    _cached_record_count_1 = None
    _cached_messages_1 = None
    _cached_record_count_2 = None
    _cached_messages_2 = None

    def setUp(self):
        # Restore or clear the shared StartDateTest cache with this class's
        # own snapshot so setUp's condition works correctly.
        StartDateTest.record_count_by_stream_1 = AftershipStartDateTest._cached_record_count_1
        StartDateTest.synced_messages_by_stream_1 = AftershipStartDateTest._cached_messages_1
        StartDateTest.record_count_by_stream_2 = AftershipStartDateTest._cached_record_count_2
        StartDateTest.synced_messages_by_stream_2 = AftershipStartDateTest._cached_messages_2
        super().setUp()

        AftershipStartDateTest._cached_record_count_1 = StartDateTest.record_count_by_stream_1
        AftershipStartDateTest._cached_messages_1 = StartDateTest.synced_messages_by_stream_1
        AftershipStartDateTest._cached_record_count_2 = StartDateTest.record_count_by_stream_2
        AftershipStartDateTest._cached_messages_2 = StartDateTest.synced_messages_by_stream_2

    @staticmethod
    def name():
        return "tap_tester_aftership_start_date_test"

    def expected_stream_names(self):
        return super().expected_stream_names().difference(NO_READ_PERMISSION_STREAMS)

    def streams_to_test(self):
        # streams to exclude due to insufficient data or tested separately
        streams_to_exclude = {
            "courier_connections",
            "orders",
            "products",
            "fulfillments",
            "shipping_rates",
            "shipping_labels",
            "shipping_manifests",
            "shipping_couriers",
            "cancel_labels",
            "pickups",
            "cancel_pickups",
            "shipper_accounts",
            "couriers",
            "trackings",  # tracking data seems to age out quickly
        }
        return self.expected_stream_names().difference(streams_to_exclude)

    @property
    def start_date_1(self):
        return "2020-01-01T00:00:00Z"
    @property
    def start_date_2(self):
        return "2026-01-01T00:00:00Z"

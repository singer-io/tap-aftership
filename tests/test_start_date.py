from base import aftershipBaseTest
from tap_tester.base_suite_tests.start_date_test import StartDateTest


class aftershipStartDateTest(StartDateTest, aftershipBaseTest):
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
        StartDateTest.record_count_by_stream_1 = aftershipStartDateTest._cached_record_count_1
        StartDateTest.synced_messages_by_stream_1 = aftershipStartDateTest._cached_messages_1
        StartDateTest.record_count_by_stream_2 = aftershipStartDateTest._cached_record_count_2
        StartDateTest.synced_messages_by_stream_2 = aftershipStartDateTest._cached_messages_2
        super().setUp()

        aftershipStartDateTest._cached_record_count_1 = StartDateTest.record_count_by_stream_1
        aftershipStartDateTest._cached_messages_1 = StartDateTest.synced_messages_by_stream_1
        aftershipStartDateTest._cached_record_count_2 = StartDateTest.record_count_by_stream_2
        aftershipStartDateTest._cached_messages_2 = StartDateTest.synced_messages_by_stream_2

    @staticmethod
    def name():
        return "tap_tester_aftership_start_date_test"

    def streams_to_test(self):
        # streams to exclude from the start date test due to access or insufficient data
        streams_to_exclude = set({
            "courier_connections",
            "item_returns",
            "item_tags",
            "query_claims",
            "query_coverages",
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
            "locations",
            "couriers",
            # Tested separately with dates that produce differing record counts
            "trackings"
        })
        return self.expected_stream_names().difference(streams_to_exclude)

    @property
    def start_date_1(self):
        return "2020-01-01T00:00:00Z"
    @property
    def start_date_2(self):
        return "2026-01-01T00:00:00Z"


class aftershipTrackingsStartDateTest(StartDateTest, aftershipBaseTest):
    """Start date test specifically for trackings.

    The trackings stream has records starting from 2026-02-06, so the
    general test's start_date_2 (2026-01-01) yields the same 60 records as
    start_date_1. Use dates where start_date_2 (2026-02-08) cuts the result
    to 3 records while start_date_1 (2020-01-01) returns all 60.
    """
    _cached_record_count_1 = None
    _cached_messages_1 = None
    _cached_record_count_2 = None
    _cached_messages_2 = None

    def setUp(self):
        StartDateTest.record_count_by_stream_1 = aftershipTrackingsStartDateTest._cached_record_count_1
        StartDateTest.synced_messages_by_stream_1 = aftershipTrackingsStartDateTest._cached_messages_1
        StartDateTest.record_count_by_stream_2 = aftershipTrackingsStartDateTest._cached_record_count_2
        StartDateTest.synced_messages_by_stream_2 = aftershipTrackingsStartDateTest._cached_messages_2
        super().setUp()

        aftershipTrackingsStartDateTest._cached_record_count_1 = StartDateTest.record_count_by_stream_1
        aftershipTrackingsStartDateTest._cached_messages_1 = StartDateTest.synced_messages_by_stream_1
        aftershipTrackingsStartDateTest._cached_record_count_2 = StartDateTest.record_count_by_stream_2
        aftershipTrackingsStartDateTest._cached_messages_2 = StartDateTest.synced_messages_by_stream_2

    @staticmethod
    def name():
        return "tap_tester_aftership_trackings_start_date_test"

    def streams_to_test(self):
        return {"trackings"}

    @property
    def start_date_1(self):
        return "2020-01-01T00:00:00Z"

    @property
    def start_date_2(self):
        return "2026-02-08T00:00:00Z"

"""Test tap discovery mode and metadata."""
from base import aftershipBaseTest
from tap_tester.base_suite_tests.discovery_test import DiscoveryTest


class aftershipDiscoveryTest(DiscoveryTest, aftershipBaseTest):
    """Test tap discovery mode and metadata conforms to standards."""

    @staticmethod
    def name():
        return "tap_tester_aftership_discovery_test"

    def streams_to_test(self):
        return self.expected_stream_names()


"""Test tap discovery mode and metadata."""
from tap_tester.base_suite_tests.discovery_test import DiscoveryTest
from tap_tester import menagerie

from base import AftershipBaseTest, NO_READ_PERMISSION_STREAMS


class AftershipDiscoveryTest(DiscoveryTest, AftershipBaseTest):
    """Test tap discovery mode and metadata conforms to standards."""

    @staticmethod
    def name():
        return "tap_tester_aftership_discovery_test"

    def expected_stream_names(self):
        return super().expected_stream_names().difference(NO_READ_PERMISSION_STREAMS)

    def streams_to_test(self):
        return self.expected_stream_names()

    def test_parent_stream(self):
        """
        Test that each stream's metadata correctly includes the expected parent tap stream ID.

        For each stream in `streams_to_test`, this test:
        - Retrieves the expected parent tap stream ID from test expectations.
        - Retrieves the actual metadata from the found catalog.
        - Verifies that the metadata contains the `PARENT_TAP_STREAM_ID` key (except for the 'accounts' stream).
        - Confirms that the actual parent tap stream ID matches the expected value.
        """
        for stream in self.streams_to_test():
            with self.subTest(stream=stream):
                expected_parent_stream_name = self.expected_parent_tap_stream(stream)
                expected_parent_stream_id = None
                if expected_parent_stream_name:
                    parent_catalog = next(
                        (clog for clog in self.found_catalogs if clog["stream_name"] == expected_parent_stream_name),
                        None
                    )
                    expected_parent_stream_id = parent_catalog["tap_stream_id"] if parent_catalog else None

                # gather results
                catalog = next(clog for clog in self.found_catalogs if clog["stream_name"] == stream)
                metadata = menagerie.get_annotated_schema(self.conn_id, catalog['stream_id'])["metadata"]
                stream_properties = [item for item in metadata if item.get("breadcrumb") == []]
                self.assertTrue(stream_properties, msg="root metadata not found")
                root_meta = stream_properties[0].get("metadata", {})
                actual_parent_tap_stream_id = root_meta.get(self.PARENT_TAP_STREAM_ID)

                if expected_parent_stream_id is None:
                    self.assertNotIn(self.PARENT_TAP_STREAM_ID, root_meta,
                                     msg=f"{stream} should not have a parent-tap-stream-id")
                else:
                    self.assertIn(self.PARENT_TAP_STREAM_ID, root_meta,
                                  msg=f"{stream} should have a parent-tap-stream-id")
                    self.assertIsInstance(actual_parent_tap_stream_id, str,
                                          msg="parent-tap-stream-id should be a string")

                # equality check
                self.assertEqual(expected_parent_stream_id, actual_parent_tap_stream_id,
                                 msg=f"verify {expected_parent_stream_id} is saved in metadata as parent-tap-stream-id")

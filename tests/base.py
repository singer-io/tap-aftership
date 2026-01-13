import copy
import os
import unittest
from datetime import datetime as dt
from datetime import timedelta

import dateutil.parser
import pytz
from tap_tester import connections, menagerie, runner
from tap_tester.logger import LOGGER
from tap_tester.base_suite_tests.base_case import BaseCase


class aftershipBaseTest(BaseCase):
    """Setup expectations for test sub classes.

    Metadata describing streams. A bunch of shared methods that are used
    in tap-tester tests. Shared tap-specific methods (as needed).
    """
    start_date = "2019-01-01T00:00:00Z"
    PARENT_TAP_STREAM_ID = "parent-tap-stream-id"

    @staticmethod
    def tap_name():
        """The name of the tap."""
        return "tap-aftership"

    @staticmethod
    def get_type():
        """The name of the tap."""
        return "platform.aftership"

    @classmethod
    def expected_metadata(cls):
        """The expected streams and metadata about the streams."""
        return {
            "trackings": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "updated_at" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "couriers": {
                cls.PRIMARY_KEYS: { "slug" },
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "courier_connections": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "updated_at" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "item_returns": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "item_tags": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "created_at" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "query_claims": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "updated_at" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "query_coverages": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "updated_at" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "stores": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "updated_at" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "orders": {
                cls.PRIMARY_KEYS: { "id", "store_id" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "updated_at" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100,
                cls.PARENT_TAP_STREAM_ID: "stores"
            },
            "products": {
                cls.PRIMARY_KEYS: { "id", "store_id" },
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100,
                cls.PARENT_TAP_STREAM_ID: "stores"
            },
            "fulfillments": {
                cls.PRIMARY_KEYS: { "id", "store_id", "order_id" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "updated_at" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100,
                cls.PARENT_TAP_STREAM_ID: "orders"
            },
            "memberships": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "roles": {
                cls.PRIMARY_KEYS: { "code" },
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "shipping_rates": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "updated_at" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "shipping_labels": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "updated_at" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "shipping_manifests": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "updated_at" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "shipping_couriers": {
                cls.PRIMARY_KEYS: { "slug" },
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "cancel_labels": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "updated_at" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "pickups": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "updated_at" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "cancel_pickups": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "updated_at" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "shipper_accounts": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "updated_at" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "locations": {
                cls.PRIMARY_KEYS: { "location_id" },
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            }
        }

    @staticmethod
    def get_credentials():
        """Authentication information for the test account."""
        credentials_dict = {}
        creds = {'api_key': 'TAP_AFTERSHIP_API_KEY'}

        for cred in creds:
            credentials_dict[cred] = os.getenv(creds[cred])

        return credentials_dict

    def get_properties(self, original: bool = True):
        """Configuration of properties required for the tap."""
        return_value = {
            "start_date": "2022-07-01T00:00:00Z"
        }
        if original:
            return return_value

        return_value["start_date"] = self.start_date
        return return_value

    def expected_parent_tap_stream(self, stream=None):
        """return a dictionary with key of table name and value of parent stream"""
        parent_stream = {
            table: properties.get(self.PARENT_TAP_STREAM_ID, None)
            for table, properties in self.expected_metadata().items()}
        if not stream:
            return parent_stream
        return parent_stream[stream]
